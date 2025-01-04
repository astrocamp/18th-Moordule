# Create your models here.
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
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
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    HOBBY_CHOICES = [
        ("eating", "吃飯"),
        ("drinking", "喝酒"),
        ("singing", "唱歌"),
        ("sports", "運動"),
        ("movies", "電影"),
        ("discussion", "討論"),
    ]
    CITIES_CHOICES = [
        ("Taipei", "臺北市"),
        ("NewTaipei", "新北市"),
        ("Keelung", "基隆市"),
        ("Taoyuan", "桃園市"),
        ("Hsinchu_City", "新竹市"),
        ("Hsinchu", "新竹縣"),
        ("Miaoli", "苗栗縣"),
        ("Taichung", "臺中市"),
        ("Changhua", "彰化縣"),
        ("Nantou", "南投縣"),
        ("Yunlin", "雲林縣"),
        ("Chiayi_City", "嘉義市"),
        ("Chiayi", "嘉義縣"),
        ("Tainan", "臺南市"),
        ("Kaohsiung", "高雄市"),
        ("Pingtung", "屏東縣"),
        ("Yilan", "宜蘭縣"),
        ("Hualien", "花蓮縣"),
        ("Taitung", "臺東縣"),
        ("Penghu", "澎湖縣"),
        ("Kinmen", "金門縣"),
        ("Lienchiang", "連江縣"),
    ]
    bio = models.TextField(
        verbose_name="自我介紹", blank=True, null=True, help_text="介紹一下你自己"
    )
    password_changed_at = models.DateTimeField(null=True, blank=True)
    username = models.CharField("站內用戶名稱", max_length=150, blank=True, null=True)
    email = models.EmailField("電子郵件", max_length=255, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    avatar = models.ImageField("頭像", upload_to="media/", blank=True, null=True)
    live_in = models.CharField(
        "居住地", choices=CITIES_CHOICES, max_length=100, blank=True, null=True
    )
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
    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
