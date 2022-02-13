from django.urls import path

from . import views

# Blog application URLs

app_name = 'store'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='index'),
    path('<category>/', views.CategoryProductListView.as_view(), name='category_products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<category>/<subcategory>/<style>/', views.ProductListView.as_view(), name='products'),
]