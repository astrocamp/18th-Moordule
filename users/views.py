from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from users.models import CustomUser

from .forms import CustomUserChangeForm, UserRegistrationForm

# Create your views here.


@login_required
def member_view(request: HttpRequest):
    return render(request, "users/account.html")


@login_required
def password_change_view(request):
    if request.method == "GET":
        return render(request, "users/components/password_change_form.html")
    else:
        user = request.user
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password1")
        confirm_password = request.POST.get("new_password2")

        if not user.check_password(old_password):
            return HttpResponse(
                '<p class="text-red-500 text-sm mt-1">舊密碼輸入有誤</p>'
            )

        if new_password != confirm_password:
            return HttpResponse('<p class="text-red-500 text-sm mt-1">密碼不一致</p>')

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)
        account_url = reverse("users:account")
        return HttpResponse("", headers={"HX-Redirect": account_url})


def signup_view(request: HttpRequest):

    meetups = [
        {
            "title": "Js Meetup",
            "category": "Programming",
            "description": "Join us for a Js programming meetup",
            "link": "https://www.meetup.com/python-meetup/",
            "start_time": "2024-12-18",
        },
        {
            "title": "Python Meetup",
            "category": "Programming",
            "description": "Join us for a Python programming meetup",
            "link": "https://www.meetup.com/python-meetup/",
            "start_time": "2024-12-18",
        },
    ]
    form = UserRegistrationForm()
    return render(request, "users/signup.html", {"meetups": meetups, "form": form})


@never_cache
def signin_view(request: HttpRequest):
    meetups = [
        {
            "title": "Js Meetup",
            "category": "Programming",
            "description": "Join us for a Js programming meetup",
            "link": "https://www.meetup.com/python-meetup/",
            "start_time": "2024-12-18",
        },
        {
            "title": "Python Meetup",
            "category": "Programming",
            "description": "Join us for a Python programming meetup",
            "link": "https://www.meetup.com/python-meetup/",
            "start_time": "2024-12-18",
        },
    ]
    return render(request, "users/signin.html", {"meetups": meetups})


@require_POST
def user_create_view(request: HttpRequest):

    meetups = [
        {
            "title": "Js Meetup",
            "category": "Programming",
            "description": "Join us for a Js programming meetup",
            "link": "https://www.meetup.com/python-meetup/",
            "start_time": "2024-12-18",
        },
        {
            "title": "Python Meetup",
            "category": "Programming",
            "description": "Join us for a Python programming meetup",
            "link": "https://www.meetup.com/python-meetup/",
            "start_time": "2024-12-18",
        },
    ]
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        signin_url = reverse("users:signin")
        return HttpResponse("", headers={"HX-Redirect": signin_url})

    return render(
        request,
        "users/components/signup_form.html",
        {"meetups": meetups, "form": form},
    )


@require_POST
def login_view(request: HttpRequest):
    meetups = [
        {
            "title": "Js Meetup",
            "category": "Programming",
            "description": "Join us for a Js programming meetup",
            "link": "https://www.meetup.com/python-meetup/",
            "start_time": "2024-12-18",
        },
        {
            "title": "Python Meetup",
            "category": "Programming",
            "description": "Join us for a Python programming meetup",
            "link": "https://www.meetup.com/python-meetup/",
            "start_time": "2024-12-18",
        },
    ]

    email = request.POST.get("email")
    password = request.POST.get("password")

    user = authenticate(
        request,
        username=email,
        password=password,
    )

    if user is not None:
        login(request, user)
        account_url = reverse("users:account")
        return HttpResponse("", headers={"HX-Redirect": account_url})

    return render(
        request,
        "users/components/signin_form.html",
        {
            "meetups": meetups,
            "form": {
                "errors": ["電子郵件或密碼錯誤"],
                "data": {"email": email},  # 保留用戶輸入的 email
            },
        },
    )


def clear_errors(request):
    return HttpResponse("")


@login_required
def account_view(request: HttpRequest):
    user = CustomUser.objects.get(pk=request.user.pk)
    return render(request, "users/member.html", {"user": user})


@login_required
def edit_view(request: HttpRequest):
    # 獲取當前登入用戶
    user = request.user

    if request.method == "POST":
        # 使用 POST 數據和用戶實例初始化表單
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            # 如果表單數據有效，保存用戶資料
            form.save()
    else:
        # 如果是 GET 請求，顯示當前用戶數據
        form = CustomUserChangeForm(instance=user)

    return render(request, "users/components/user_form.html", {"form": form})
