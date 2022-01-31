import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .cart import Cart
from .models import Order
from store.models import Product
from .forms import CartAddProductForm
from django.forms.models import model_to_dict

# Create your views here.

def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    data = json.loads(str(request.body, encoding='utf-8'))
    print(data)
    form = CartAddProductForm(data)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], size=cd['size'], update_quantity=cd['update'])
        checkout_params = cart.get_checkout_params()
        return JsonResponse({
            'total_products': len(cart),
            'item_total_price': cart.get_item_total_price(product_id=product.id, size=cd['size']),
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
        sizes = item['size']
        for size in sizes:
            sizes[size]['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': sizes[size]['quantity'],
                                            'update': True,
                                            'size': size
                                        })
            sizes[size]['total_price'] = item['price'] * sizes[size]['quantity']
    return render(request, 'cart/detail.html',
                 {'cart': cart})
    
def CartRemove(request, product_id=None, size=None):
    print(size)
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product, size=size)
    return redirect('cart:detail')

def Checkout(request):
    cart = Cart(request)
    items = []
    for item in cart:
        item['product'] = model_to_dict(
            item['product'],
            fields=['id','name','slug','description','sub_category']
        )
        items.append(item)
    if(len(items) > 0):
        tax = cart.get_tax()
        total_price = cart.get_total_price()
        Order.objects.create(tax=tax, total_price=total_price, items=items)
        cart.clear()
    return render(request, 'cart/checkout.html')
