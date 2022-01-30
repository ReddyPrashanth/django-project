import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .cart import Cart
from store.models import Product
from .forms import CartAddProductForm

# Create your views here.

def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    data = json.loads(str(request.body, encoding='utf-8'))
    form = CartAddProductForm(data)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        checkout_params = cart.get_checkout_params()
        return JsonResponse({
            'total_products': len(cart),
            'item_total_price': cart.get_item_total_price(product.id),
            'sub_total': checkout_params['sub_total'],
            'tax': checkout_params['tax'],
            'total': checkout_params['total']
        }, status=200)
    else:
        print(form.errors)
        return JsonResponse({'message': 'Unable to add to cart. Please try again.'}, status=400)

def TotalProducts(request):
    cart = Cart(request)
    return JsonResponse({'total_products': len(cart)}, status=200)

def CartDetail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    return render(request, 'cart/detail.html',
                 {'cart': cart})
    
def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart:detail')
