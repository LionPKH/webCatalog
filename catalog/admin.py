from django.contrib import admin
from .models import Category, Product, Banner, Model3D

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


@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order', 'auto_rotate', 'created_at')
    list_filter = ('is_active', 'auto_rotate')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'headline', 'description')
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'headline', 'description', 'glb_file', 'poster'),
        }),
        ('Параметры показа', {
            'fields': ('auto_rotate', 'rotation_speed', 'camera_orbit', 'exposure'),
            'classes': ('collapse',),
        }),
        ('Управление', {
            'fields': ('is_active', 'order'),
        }),
    )
