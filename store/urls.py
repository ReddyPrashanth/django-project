from django.urls import path

from . import views

# Blog application URLs

app_name = 'store'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='index'),
    path('<category>/', views.products, name='category_products'),
    path('<category>/<subcategory>/<style>/', views.ProductListView.as_view(), name='products'),
]