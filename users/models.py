from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractUser):
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    live_in = models.CharField(max_length=255, blank=True, null=True)
    hobby_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
