import django.forms as forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["password_mismatch"] = "兩次輸入的密碼不相符"

    email = forms.EmailField(
        error_messages={
            "unique": "電子郵件已經被使用",
            "invalid": "請輸入有效的電子郵件地址",
            "required": "請輸入電子郵件",
        },
        widget=forms.EmailInput(
            attrs={
                "type": "email",
                "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                "title": "請輸入有效的電子郵件地址",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")


class CustomUserChangeForm(forms.ModelForm):
    """個人資料編輯表單 - 包含選填欄位"""

    class Meta:
        model = CustomUser
        fields = ("username", "gender", "birth_date",  "live_in", "hobby")