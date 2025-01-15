from django.db import models
from users.models import CustomUser as User

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=255, unique=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField( verbose_name="交易金額")
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.order_id} - {self.amount} {self.currency}"


class Wallet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    balence = models.IntegerField(verbose_name="餘額", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
