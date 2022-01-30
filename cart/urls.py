from django.urls import path, include

from . import views

# Blog application URLs

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetail, name="detail"),
    path('total-products/', views.TotalProducts, name="total_products"),
    path('add/<int:product_id>', views.CartAdd, name="add"),
    path('remove/<int:product_id>', views.CartRemove, name="remove"),
]