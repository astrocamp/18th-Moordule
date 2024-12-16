from django.db import models

# Create your models here.
class Payments(models.Model):
    created_at = models.DateTimeField(),
    amount = models.IntegerField(verbose_name="交易金額"),
    order_no = models.CharField(unique=True),
    # status = models.Choices(value=str),

class Wallets(models.Model):
    created_at = models.DateTimeField(),
    balence = models.IntegerField(verbose_name="餘額"),