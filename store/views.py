from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from .models import Category, Product, Size
# Create your views here.

class CategoryListView(ListView):
    template_name = 'store/index.html'
    model = Category
    
    def get_queryset(self):
        return self.model.objects.all()

def products(request, category, subcategory=None, style=None):
    return render(
        request, 
        'store/product_list.html'
    )
    
class ProductListView(ListView):
    template_name = 'store/product_list.html'
    model = Product
    paginate_by = 24
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs) 
        sizes = self.get_sizes()
        context['sizes'] = sizes
        return context
    
    def get_sizes(self):
        return Size.objects.all().values('id', 'name', 'slug')
    
    def get_queryset(self):
        query_params = self.request.GET
        category = self.kwargs.get('category')
        subcategory = self.kwargs.get('subcategory')
        style = self.kwargs.get('style')
        query = Q(category__slug=category, sub_category__slug=subcategory, styles__slug=style)
        size = query_params.get('size', False)
        min_price = query_params.get('min_price', False)
        max_price = query_params.get('max_price', False)
        if(size):
            query &= Q(productinventory__inventorysize__size_id=size)
        if(min_price and max_price):
            query = Q(price__gte=min_price, price__lte=max_price)
        return Product.objects.filter(query).distinct()