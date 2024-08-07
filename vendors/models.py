from django.db import models
from django.db.models import Avg, F
# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_vendor_metrics()

    def update_vendor_metrics(self):
        vendor = self.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

        if completed_orders.exists():
            vendor.on_time_delivery_rate = completed_orders.filter(delivery_date__lte=F('delivery_date')).count() / completed_orders.count()
            vendor.quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0
            vendor.average_response_time = completed_orders.annotate(response_time=F('acknowledgment_date') - F('issue_date')).aggregate(Avg('response_time'))['response_time__avg'].total_seconds() / 3600 if completed_orders.filter(acknowledgment_date__isnull=False).exists() else 0.0
            vendor.fulfillment_rate = completed_orders.count() / PurchaseOrder.objects.filter(vendor=vendor).count()

        vendor.save()
    
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Performance on {self.date} for {self.vendor.name}"