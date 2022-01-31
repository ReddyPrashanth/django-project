from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Category, Product, Size, ProductInventory
# Create your views here.

class CategoryListView(ListView):
    template_name = 'store/index.html'
    model = Category
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured"] = ProductInventory.objects.filter(featured = True)[:10]
        return context

    def get_queryset(self):
        return self.model.objects.all()
    
class ProductView(ListView):
    template_name = 'store/product_list.html'
    model = Product
    paginate_by = 24
    
    def get_sizes(self):
        return Size.objects.all().values('id', 'name', 'slug')
    
    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs) 
        sizes = self.get_sizes()
        context['sizes'] = sizes
        return context
    
    def get_products(self,query_params, kwargs):
        category = kwargs.get('category')
        subcategory = kwargs.get('subcategory', False)
        style = kwargs.get('style', False)
        query = Q(category__slug=category)
        if subcategory:
            query &= Q(sub_category__slug=subcategory)
        if style:
            query &= Q(styles__slug=style)
        size = query_params.get('size', False)
        min_price = query_params.get('min_price', False)
        max_price = query_params.get('max_price', False)
        if(size):
            query &= Q(productinventory__inventorysize__size_id=size)
        if(min_price and max_price):
            query = Q(price__gte=min_price, price__lte=max_price)
        return self.model.objects.filter(query).distinct()

class CategoryProductListView(ProductView):
    def get_queryset(self):
        query_params = self.request.GET
        return self.get_products(query_params, self.kwargs)
    
    
class ProductListView(ProductView):
    def get_queryset(self):
        query_params = self.request.GET
        return super(ProductListView, self).get_products(query_params, self.kwargs)
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sizes"] = self.get_sizes()
        context["featured"] = ProductInventory.objects.filter(featured = True)[:5]
        return context

    def get_sizes(self):
        return Size.objects.all().values('id', 'name', 'slug')
    