from django.shortcuts import render
from django.http import HttpResponseBadRequest
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
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs) 
        sizes = self.get_sizes()
        print(sizes)
        context['sizes'] = sizes
        return context
    
    def get_sizes(self):
        return Size.objects.all().values('id', 'name', 'slug')
    
    def get_queryset(self):
        category = self.kwargs.get('category')
        subcategory = self.kwargs.get('subcategory')
        style = self.kwargs.get('style')
        return Product.objects.filter(category__slug=category, sub_category__slug=subcategory, styles__slug=style)