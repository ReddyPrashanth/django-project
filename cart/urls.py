from django.urls import path, include

from . import views

# Blog application URLs

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetail, name="detail"),
    path('review-and-pay/', views.ReviewAndPay, name="review_and_pay"),
    path('place-order/', views.PlaceOrder, name="place_order"),
    path('total-products/', views.TotalProducts, name="total_products"),
    path('checkout/', views.Checkout, name="checkout"),
    path('add/<int:product_id>', views.CartAdd, name="add"),
    path('remove/<int:product_id>/<size>', views.CartRemove, name="remove"),
]