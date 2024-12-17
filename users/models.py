# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.


class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "hobbies"
        verbose_name = "興趣"

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    live_in = models.CharField(max_length=255, blank=True, null=True)
    hobby_id = models.ForeignKey(
        Hobby, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
