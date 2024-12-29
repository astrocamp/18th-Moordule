# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager
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


class CustomUserManager(UserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # 因為 AbstractUser 需要 username，所以我們用 email 當作 username
        return super().create_user(
            username=email,  # username 欄位還是需要值
            email=email,
            password=password,
            **extra_fields
        )


class CustomUser(AbstractUser):

    GENDER_CHOICES = [
        ("male", "Male"),  # ('存儲值', '顯示值')
        ("female", "Female"),
        ("other", "Other"),
    ]

    HOBB_CHOICES = [
        ("eating", "吃飯"),
        ("drinking", "喝酒"),
        ("sleeping", "唱歌"),
        ("sports", "運動"),
        ("movies", "電影"),
        ("discussion", "討論"),
    ]
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    live_in = models.CharField(max_length=255, blank=True, null=True)

    hobby = models.CharField(
        max_length=255, choices=HOBB_CHOICES, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
