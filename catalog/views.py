from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Banner
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    # Достаем все товары из базы
    products = Product.objects.all()
    banners = Banner.objects.all()

    # Передаем их в словарь context, чтобы использовать в HTML
    context = {
        'products': products,
        'banners': banners,
    }
    return render(request, 'catalog/index.html', context)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        # Если выбрана категория — фильтруем по ней
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(categories=category)
    else:
        # Если категория не выбрана — показываем только популярные
        products = products.filter(is_popular=True)

    return render(request, 'catalog/catalog_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request, pk):
    # Пытаемся найти товар по ID или выдаем 404 ошибку
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


@staff_member_required
@csrf_exempt
def process_image_ai(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        prompt = product.ai_prompt

        if not product.image or not prompt:
            return JsonResponse({'error': 'Нужно фото и промпт'}, status=400)

        # ПРИМЕР запроса к API (структура зависит от документации Nano Banana)
        api_url = "https://api.nanobanana.com/v1/process"  # Замени на реальный URL
        headers = {"Authorization": "AIzaSyDuyi_13RyhfKN-DZMN5UVIfe5rdnzVoFo"}

        with open(product.image.path, 'rb') as f:
            files = {'image': f}
            data = {'prompt': prompt}
            response = requests.post(api_url, headers=headers, files=files, data=data)

        if response.status_code == 200:
            # Предположим, API возвращает саму картинку
            new_image_content = response.content
            # Сохраняем обновленное фото
            file_name = f"ai_{product.image.name.split('/')[-1]}"
            product.image.save(file_name, ContentFile(new_image_content), save=True)

            return JsonResponse({'success': True, 'url': product.image.url})

        return JsonResponse({'error': 'Ошибка API'}, status=500)
