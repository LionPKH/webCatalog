from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Пустая строка означает главную страницу
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('process-ai/<int:product_id>/', views.process_image_ai, name='process_ai'),
]
