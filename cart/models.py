from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

# Create your models here.

class Order(models.Model):
    ordered_date = models.DateField(default=date.today)
    order_id = models.UUIDField(editable=False, serialize=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    delivery_date = models.DateField(null=True)
    order_completed = models.BooleanField(default=False)
    tax = models.FloatField()
    total_price = models.FloatField()
    order_cancelled = models.BooleanField(default=False)
    items = models.JSONField()
    payment_intent = models.CharField(max_length=50, null=True)
    payment_intent_client_secret = models.CharField(max_length=80, null=True)
    payment_succeded = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    
class DeliveryOption(models.Model):
    slug = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField()
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    sort_order = models.PositiveSmallIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['slug'], name='idx_slug_delivery_option'),
        ]
        ordering = ['sort_order']
