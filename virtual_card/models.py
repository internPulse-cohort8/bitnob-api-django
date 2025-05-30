from django.db import models
from django.conf import settings

class VirtualCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bitnob_card_id = models.CharField(max_length=100, unique=True)
    card_brand = models.CharField(max_length=50, blank=True)
    card_type = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, default="pending")
    reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.card_brand} {self.bitnob_card_id} ({self.status})"