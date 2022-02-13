import uuid
from django.conf import settings
from store.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        order_id = self.session.get('order_id')
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
            order_id = self.session['order_id'] = str(uuid.uuid4())
        self.cart = cart
        self.order_id = order_id
        
    def add(self, product, quantity=1, size='small', update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'size': {
                    size: {
                        'quantity': 0
                    }
                }
            }
        item = self.cart[product_id]
        size_exists = size in item['size']
        if update_quantity and size_exists:
            item['quantity'] = item['quantity'] - item['size'][size]['quantity'] + quantity
            item['size'][size]['quantity'] = quantity
        else:
            item['quantity'] += quantity
            if size_exists:
                item['size'][size]['quantity'] += quantity
            else:
                item['size'][size] = {
                    'quantity': quantity
                }
        self.save()
        
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def remove(self, product, size):
        product_id = str(product.id)
        if product_id in self.cart and size in self.cart[product_id]['size']:
            if len(self.cart[product_id]['size']) > 1:
                self.cart[product_id]['quantity'] -= self.cart[product_id]['size'][size]['quantity']
                del self.cart[product_id]['size'][size]
            else:
                del self.cart[product_id]                
            self.save()
            
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        
        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['quantity'] * item['price']
            yield item
            
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_sub_total(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def get_tax(self):
        return self.get_sub_total() * 10/100
    
    def get_total_price(self):
        total_price = self.get_sub_total() + self.get_tax()
        return float('{0:.2f}'.format(total_price))
    
    def get_checkout_params(self):
        sub_total = self.get_sub_total()
        tax = sub_total * 10/100
        total_price = float('{0:.2f}'.format(sub_total+tax))
        return {'sub_total': sub_total, 'tax': tax, 'total': total_price}
    
    def get_item_total_price(self, product_id, size):
        item = self.cart.get(str(product_id))
        return item['size'][size]['quantity'] * float(item['price'])
    
    def get_order_id(self):
        return self.order_id
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True