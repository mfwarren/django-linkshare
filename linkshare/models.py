from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SalesReport(models.Model):
    user=models.ForeignKey(User)
    date = models.DateField()

    advertiser_id = models.CharField(max_length=32)
    advertiser = models.CharField(max_length=64)
    impressions = models.FloatField()
    clicks = models.FloatField()
    ctr = models.FloatField()
    orders = models.FloatField()
    orders_per_click = models.FloatField()
    epc = models.FloatField()
    items = models.FloatField()
    cancelled_items = models.FloatField()
    sales = models.FloatField()
    baseline_commissions = models.FloatField()
    adjusted_commissions = models.FloatField()
    actual_commissions = models.FloatField()
