from django.db import models
from datetime import datetime

# Create your models here.

class BaseModel(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    description = models.TextField()
    sort_order = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(default=datetime.now)
    
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