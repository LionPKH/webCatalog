import os

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Min, Max
from django.core.paginator import Paginator
import requests

from .models import Product, Category, Banner, Model3D


# --- Конфигурация сортировок (используется и во вьюхе, и в шаблоне) ---
SORT_OPTIONS = {
    'popular':    {'label': 'Сначала популярные', 'order': ('-is_popular', '-id')},
    'newest':     {'label': 'Сначала новые',       'order': ('-id',)},
    'price_asc':  {'label': 'Цена: по возрастанию', 'order': ('price', '-id')},
    'price_desc': {'label': 'Цена: по убыванию',    'order': ('-price', '-id')},
    'name':       {'label': 'По названию (А–Я)',    'order': ('name',)},
}
DEFAULT_SORT = 'popular'


def _apply_filters(qs, request):
    """Общая логика: поиск, фильтр по цене и сортировка для каталога."""
    q = (request.GET.get('q') or '').strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # Диапазон цен
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    try:
        if min_price not in (None, ''):
            qs = qs.filter(price__gte=float(min_price))
    except (TypeError, ValueError):
        pass
    try:
        if max_price not in (None, ''):
            qs = qs.filter(price__lte=float(max_price))
    except (TypeError, ValueError):
        pass

    # Только популярные
    if request.GET.get('only_popular') in ('1', 'true', 'on'):
        qs = qs.filter(is_popular=True)

    # Сортировка
    sort_key = request.GET.get('sort') or DEFAULT_SORT
    if sort_key not in SORT_OPTIONS:
        sort_key = DEFAULT_SORT
    qs = qs.order_by(*SORT_OPTIONS[sort_key]['order'])

    return qs, {
        'q': q,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'only_popular': request.GET.get('only_popular') in ('1', 'true', 'on'),
        'sort': sort_key,
    }


def index(request):
    products = Product.objects.all().order_by('-is_popular', '-id')[:12]
    banners = Banner.objects.filter(is_active=True)
    categories = Category.objects.all()
    # Все активные 3D-модели — будут стэком на фоне главной
    models3d_bg = list(
        Model3D.objects.filter(is_active=True)
        .order_by('order', '-created_at')
    )

    context = {
        'products': products,
        'banners': banners,
        'categories': categories,
        'models3d_bg': models3d_bg,
    }
    return render(request, 'catalog/index.html', context)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    base_qs = Product.objects.all().distinct()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        base_qs = base_qs.filter(categories=category)

    # Применяем поиск/фильтры/сортировку
    products_qs, applied = _apply_filters(base_qs, request)

    # Граничные значения цен (для placeholder в форме)
    price_bounds = Product.objects.aggregate(min=Min('price'), max=Max('price'))

    # Пагинация
    paginator = Paginator(products_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Готовим список сортировок для шаблона
    sort_choices = [
        {'value': key, 'label': value['label']}
        for key, value in SORT_OPTIONS.items()
    ]

    # querystring без `page` (для постоянных ссылок пагинации)
    qd = request.GET.copy()
    qd.pop('page', None)
    base_querystring = qd.urlencode()

    context = {
        'category': category,
        'categories': categories,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'applied': applied,
        'sort_choices': sort_choices,
        'price_bounds': price_bounds,
        'base_querystring': base_querystring,
        'total_count': paginator.count,
    }
    return render(request, 'catalog/catalog_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Похожие товары — из тех же категорий
    related = (
        Product.objects
        .filter(categories__in=product.categories.all())
        .exclude(pk=product.pk)
        .distinct()[:4]
    )
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related': related,
    })


@staff_member_required
@csrf_exempt
def process_image_ai(request, product_id):
    """Отправка фото на обработку Nano Banana. Ключ берётся из окружения."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

    product = get_object_or_404(Product, pk=product_id)
    prompt = product.ai_prompt

    if not product.image or not prompt:
        return JsonResponse({'error': 'Нужно фото и промпт'}, status=400)

    api_key = os.environ.get('NANO_BANANA_API_KEY')
    if not api_key:
        return JsonResponse(
            {'error': 'Не задан NANO_BANANA_API_KEY в переменных окружения'},
            status=500,
        )

    api_url = os.environ.get(
        'NANO_BANANA_API_URL',
        'https://api.nanobanana.com/v1/process',
    )
    headers = {'Authorization': f'Bearer {api_key}'}

    with open(product.image.path, 'rb') as f:
        files = {'image': f}
        data = {'prompt': prompt}
        response = requests.post(api_url, headers=headers, files=files, data=data, timeout=60)

    if response.status_code == 200:
        file_name = f"ai_{product.image.name.split('/')[-1]}"
        product.image.save(file_name, ContentFile(response.content), save=True)
        return JsonResponse({'success': True, 'url': product.image.url})

    return JsonResponse({'error': 'Ошибка API'}, status=500)
