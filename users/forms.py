from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

FORM_WIDGETS = {
    "base": {
        "class": "mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-yellow-400",
    },
    "email": {
        "class": "mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-yellow-400",
        "type": "email",
        "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "title": "請輸入有效的電子郵件地址",
        "placeholder": "請輸入電子郵件",
    },
    "text": {
        "class": "mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-yellow-400",
    },
    "date": {
        "class": "mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-yellow-400",
        "type": "date",
    },
    "file": {"class": "hidden", "accept": "image/*"},
    "select": {
        "class": "mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-yellow-400"
    },
    "textarea": {
        "class": "mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-yellow-400",
        "rows": "4",
    },
}


ERROR_MESSAGES = {
    "email": {
        "unique": "電子郵件已經被使用",
        "invalid": "請輸入有效的電子郵件地址",
        "required": "請輸入電子郵件",
    },
    "username": {"required": "請輸入使用者名稱"},
    "password": {"mismatch": "兩次輸入的密碼不相符"},
}


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["password_mismatch"] = ERROR_MESSAGES["password"][
            "mismatch"
        ]

    email = forms.EmailField(
        error_messages=ERROR_MESSAGES["email"],
        widget=forms.EmailInput(attrs=FORM_WIDGETS["email"]),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")


class CustomUserChangeForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        error_messages=ERROR_MESSAGES["username"],
        widget=forms.TextInput(
            attrs={**FORM_WIDGETS["text"], "placeholder": "請輸入顯示名稱"}
        ),
    )

    birth_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs=FORM_WIDGETS["date"])
    )

    gender = forms.ChoiceField(
        choices=CustomUser.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs=FORM_WIDGETS["select"]),
    )

    live_in = forms.ChoiceField(
        choices=CustomUser.CITIES_CHOICES,
        required=False,
        widget=forms.Select(attrs=FORM_WIDGETS["select"]),
    )

    hobbies = forms.MultipleChoiceField(
        choices=CustomUser.HOBBY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = CustomUser
        fields = ["username", "birth_date", "gender", "live_in", "hobbies"]


class AboutMeForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={**FORM_WIDGETS["textarea"], "placeholder": "請介紹一下你自己"}
        ),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ["bio"]
