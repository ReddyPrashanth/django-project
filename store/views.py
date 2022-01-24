from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.generic import ListView
from .models import Category, Product
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
    
    # def get(self, request, *args, **kwargs):
    #     print(kwargs)
    #     if not (bool(kwargs.get('category', None)) or bool(kwargs.get('subcategory', None)) or bool(kwargs.get('style', None))): 
    #         return HttpResponseBadRequest()
    #     return super().get(request, *args, **kwargs)
    def get_queryset(self):
        category = self.kwargs.get('category')
        subcategory = self.kwargs.get('subcategory')
        style = self.kwargs.get('style')
        return Product.objects.filter(category__slug=category, sub_category__slug=subcategory, styles__slug=style)