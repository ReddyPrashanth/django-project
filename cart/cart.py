from django.conf import settings
from store.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
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
    
    def get_item_total_price(self, product_id):
        item = self.cart.get(str(product_id))
        return item['quantity'] * float(item['price'])
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True