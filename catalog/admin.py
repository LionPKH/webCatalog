from django.contrib import admin
from .models import Category, Product, Banner

admin.site.register(Category)
admin.site.register(Banner)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 1. Возвращаем все колонки в списке товаров
    list_display = ('name', 'display_categories', 'price')

    # 2. Возвращаем фильтры и поиск
    list_filter = ('categories', 'is_popular')
    search_fields = ('name', 'description')

    # 3. Возвращаем удобный выбор категорий
    filter_horizontal = ('categories',)

    # 4. Твоя функция для красивого вывода категорий (сохраняем её!)
    @admin.display(description='Категории')
    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])

    # 5. ДОБАВЛЯЕМ ТОЛЬКО ЭТО: подключение JS-файла для кнопки AI
    class Media:
        js = ('catalog/js/ai_button.js',)