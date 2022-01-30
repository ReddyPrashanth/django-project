from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

# Create your models here.

class Order(models.Model):
    ordered_date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    delivery_date = models.DateField(null=True)
    order_completed = models.BooleanField(default=False)
    tax = models.FloatField()
    total_price = models.FloatField()
    order_cancelled = models.BooleanField(default=False)
    items = models.JSONField()
    created_at = models.DateTimeField(blank=True, auto_now_add=True)