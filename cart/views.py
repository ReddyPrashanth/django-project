import json
import stripe
from .cart import Cart
from store.models import Product
from django.conf import settings
from django.http import JsonResponse
from .forms import CartAddProductForm
from .models import Order, DeliveryOption
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render

stripe.api_key = settings.STRIPE_KEY

# Create your views here.

def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    data = json.loads(str(request.body, encoding='utf-8'))
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
                 {'cart': cart, 'step':1})
    
def CartRemove(request, product_id=None, size=None):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product, size=size)
    return redirect('cart:detail')

def ReviewAndPay(request):
    cart = Cart(request)
    return render(request, 'cart/payment.html', {'cart': cart, 'step': 3})

def PlaceOrder(request):
    payment_intent = request.GET.get('payment_intent', None)
    client_secret = request.GET.get('payment_intent_client_secret', None)
    redirect_status = request.GET.get('redirect_status', None)
    payment_succeded = False
    if(redirect_status == 'succeeded'):
        payment_succeded = True
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
        order_id = cart.get_order_id()
        Order.objects.create(
            order_id=order_id,
            tax=tax, 
            total_price=total_price, 
            items=items, 
            payment_intent=payment_intent,
            payment_intent_client_secret=client_secret,
            payment_succeded=payment_succeded
        )
        cart.clear()
    return render(request, 'cart/order_placed.html')

def Checkout(request):
    cart = Cart(request)
    delivery_options = DeliveryOption.objects.all()
    return render(request, 'cart/checkout.html', {'cart': cart, 'step':2, 'del_options': delivery_options})

@csrf_exempt
def CreatePayment(request):
    cart = Cart(request)
    print(cart.get_order_id())
    try:
        intent = stripe.PaymentIntent.create(
            amount = int(cart.get_total_price()* 100),
            currency='usd',
            payment_method_types = ["card"],
            metadata = {
                "order_id": cart.get_order_id()
            }
        )
        return JsonResponse({'clientSecret': intent['client_secret']})
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=403)