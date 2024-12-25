# Create your models here.
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Record(models.Model):
    TYPE_CHOICES = [
        ("meetup", "聚會"),
        ("topup", "儲值"),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="records"
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    notes = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_notes(self, **kwargs):
        if self.type == "meetup":
            self.notes = {
                "topic": kwargs.get("topic", ""),
            }
        elif self.type == "topup":
            self.notes = {
                "payment_method": kwargs.get("payment_method", ""),
            }

    @property
    def topic(self):
        return self.notes.get("topic") if self.type == "meetup" else None

    @property
    def payment_method(self):
        return self.notes.get("payment_method") if self.type == "topup" else None

    class Meta:
        db_table = "records"
        verbose_name = "記錄"


class CustomUser(AbstractUser):
    HOBBY_CHOICES = [
        ("eating", "吃飯"),
        ("drinking", "喝酒"),
        ("singing", "唱歌"),
        ("sports", "運動"),
        ("movies", "電影"),
        ("discussion", "討論"),
    ]

    username = models.CharField("站內用戶名稱", max_length=150, blank=True, null=True)
    email = models.EmailField("電子郵件", max_length=255, unique=True)
    avatar = models.ImageField("頭像", upload_to="media/", blank=True, null=True)
    live_in = models.CharField("居住地", max_length=255, blank=True, null=True)
    hobbies = ArrayField(
        models.CharField(max_length=100, choices=HOBBY_CHOICES),
        blank=True,
        default=list,
        verbose_name="興趣",
    )
    created_at = models.DateTimeField("創建日期", auto_now_add=True)
    updated_at = models.DateTimeField("更新日期", auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
