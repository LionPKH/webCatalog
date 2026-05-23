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
