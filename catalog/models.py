from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    # verbose_name нужен, чтобы в админке всё было по-русски и красиво
    slug = models.SlugField(max_length=100, unique=True, null=True, verbose_name="Слаг для стиля (eng)")
    THEME_CHOICES = [
        ('winter', 'Зима'),
        ('spring', 'Весна'),
        ('summer', 'Лето'),
        ('autumn', 'Осень'),
    ]
    style_theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default='spring',
        verbose_name="Стиль оформления"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    # Привязываем товар к категории
    categories = models.ManyToManyField(Category, verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Название композиции")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    # upload_to='products/' будет сохранять картинки в папку media/products/
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    is_popular = models.BooleanField(default=False, verbose_name="Популярный товар")

    ai_prompt = models.TextField(blank=True, verbose_name="Промпт для AI (обработка фото)")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/', verbose_name="Изображение фона")
    is_active = models.BooleanField(default=True, verbose_name="Отображать на сайте?")

    class Meta:
        verbose_name = "Фото для фона главной"
        verbose_name_plural = "Фото для фона главной"

    def __str__(self):
        return f"Фоновое фото {self.id}"


class Model3D(models.Model):
    """
    3D-модель в формате .glb для витрины на сайте.
    Можно загружать новые модели через админку, менять активную, настраивать вращение и т.д.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="Название модели",
        help_text="Например: Кролик · фарфор",
    )
    headline = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Заголовок для витрины",
        help_text="Если пусто — будет использовано название",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Краткое описание",
        help_text="Текст рядом с моделью на главной",
    )
    glb_file = models.FileField(
        upload_to='models3d/',
        verbose_name="Файл .glb / .gltf",
        help_text="Бинарный glTF (.glb) — самый удобный формат",
    )
    poster = models.ImageField(
        upload_to='models3d/posters/',
        blank=True,
        null=True,
        verbose_name="Постер (превью)",
        help_text="Картинка-заглушка, пока модель грузится. Можно оставить пустым.",
    )

    # --- Параметры показа ---
    auto_rotate = models.BooleanField(
        default=True,
        verbose_name="Авто-вращение",
        help_text="Модель плавно крутится сама",
    )
    rotation_speed = models.PositiveIntegerField(
        default=12,
        verbose_name="Скорость вращения (град/сек)",
        help_text="Рекомендуется 8–20",
    )
    camera_orbit = models.CharField(
        max_length=80,
        default="0deg 80deg 105%",
        verbose_name="Стартовая орбита камеры",
        help_text="Формат model-viewer: '0deg 75deg 105%' (азимут, наклон, радиус)",
    )
    exposure = models.FloatField(
        default=0.95,
        verbose_name="Экспозиция",
        help_text="0.5 — темнее, 1.5 — ярче",
    )

    # --- Управление ---
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Показывать на сайте",
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
        help_text="Меньше — выше. Главная показывает первую активную.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "3D-модель"
        verbose_name_plural = "3D-модели"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name
