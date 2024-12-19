from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from users.models import CustomUser

from .forms import UserRegistrationForm

# Create your views here.


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
        # return HttpResponse("", headers={"HX-Push": "/"})  # 只在成功時設置 URL
    else:

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
        dashboard_url = reverse("users:dashboard", args=[user.pk])
        return HttpResponse("", headers={"HX-Redirect": dashboard_url})

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


def dashboard_view(request: HttpRequest, id):
    user = CustomUser.objects.get(pk=id)
    return render(request, "users/dashboard.html", {"user": user})
