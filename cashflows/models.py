from django.db import models


# Create your models here.
class Payments(models.Model):
    created_at = (models.DateTimeField(auto_now_add=True),)
    amount = (models.IntegerField(verbose_name="交易金額"),)
    order_no = (models.CharField(unique=True),)
    # status = models.Choices(value=str),


class Wallets(models.Model):
    created_at = (models.DateTimeField(auto_now_add=True),)
    balence = (models.IntegerField(verbose_name="餘額"),)
