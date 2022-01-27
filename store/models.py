from email.policy import default
from lib2to3.pytree import Base
from django.db import models
from datetime import datetime

# Create your models here.

class BaseModel(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    description = models.TextField()
    sort_order = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    
    class Meta:
        abstract = True
        ordering = ['sort_order']

class Category(BaseModel):

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['slug'], name='idx_slug_category')
        ]
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='uq_slug_category'),
        ]
        
class SubCategory(BaseModel):
    categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['slug'], name='idx_slug_subcategory')
        ]
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='uq_slug_subcategory'),
        ]
        
class Style(BaseModel):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)    
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['slug'], name='idx_slug_style'),
            models.Index(fields=['sub_category_id'], name='idx_sub_category_id_style')
        ]
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='uq_slug_style'),
        ]
        
class Product(BaseModel):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    styles = models.ManyToManyField(Style)
    
    def inventory(self):
        return ProductInventory.objects.filter(product_id=self.id).all()
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['slug'], name='idx_slug_product'),
            models.Index(fields=['category_id'], name='idx_category_id_product'),
            models.Index(fields=['sub_category_id'], name='idx_sub_category_id_product')
        ]
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='uq_slug_product'),
        ]
   
class Color(models.Model):
    name = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='uq_name_color'),
        ]
    
class Size(BaseModel):
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='uq_slug_size'),
        ]
    
class ProductInventory(models.Model):
    image_url = models.CharField(max_length=100,null=True)
    active = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=['product_id'], name='idx_product_id_inventory'),
            models.Index(fields=['color_id'], name='idx_color_id_inventory')
        ]

class InventorySize(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    product_inventory = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['size_id'], name='idx_size_id_inventory_size'),
            models.Index(fields=['product_inventory_id'], name='idx_inventory_id_size')
        ]