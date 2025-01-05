from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django_htmx.middleware import HtmxDetails

from activities.models import Activity as Meetup

from .forms import CustomUserChangeForm, UserRegistrationForm


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# Create your views here.


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

@login_required
def user_page_view(request, tag="member"):
    if not request.headers.get("HX-Request"):
        context = {"tag": tag}
        return render(request, "users/dashboard.html", context)

    return render(request, f"users/components/{tag}.html")


@require_POST
def upload_view(request: HttpRequest):
    image = request.FILES.get("image")
    print("uploading image")
    if image:
        # 處理圖片上傳邏輯
        # 例如：儲存到媒體目錄 or 儲存到雲端
        # image.save(f'media/uploads/{image.name}')

        return JsonResponse(
            {
                "status": "success",
                "message": "上傳成功",
                "image_url": f"/media/uploads/{image.name}",
            }
        )

    return JsonResponse({"status": "error", "message": "上傳失敗"}, status=400)


def signup_view(request: HttpRequest):

    if request.POST:
        form = UserRegistrationForm()
        if form.is_valid():
            form.save()
            signin_url = reverse("users:signin")
            return HttpResponse("", headers={"HX-Redirect": signin_url})

    meetups = Meetup.objects.filter(start_time__gte=timezone.now()).order_by(
        "start_time"
    )[:2]

    return render(request, "users/signup.html", {"meetups": meetups})


def signin_view(request: HttpRequest):
    meetups = Meetup.objects.filter(start_time__gte=timezone.now()).order_by(
        "start_time"
    )[:2]

    return render(request, "users/signin.html", {"meetups": meetups})


@require_POST
def user_create_view(request: HtmxHttpRequest):
    form = UserRegistrationForm(request.POST)
    if request.POST:
        if form.is_valid():
            form.save()
            signin_url = reverse("users:signin")
            return HttpResponse("", headers={"HX-Redirect": signin_url})

    return render(
        request,
        "users/components/signup_form.html",
        {"form": form},
    )


@require_POST
def login_view(request: HttpRequest):

    email = request.POST.get("email")
    password = request.POST.get("password")

    user = authenticate(
        request,
        username=email,
        password=password,
    )

    if user is not None:
        login(request, user)
        index_url = reverse("pages:index")
        return HttpResponse("", headers={"HX-Redirect": index_url})

    return render(
        request,
        "users/components/signin_form.html",
        {
            "form": {
                "errors": ["電子郵件或密碼錯誤"],
                "data": {"email": email},
            },
        },
    )


def clear_errors(request: HtmxHttpRequest):
    return HttpResponse("")


@login_required
def edit_view(request: HttpRequest):

    user = request.user
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            # 如果表單數據有效，保存用戶資料
            form.save()
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, "users/components/user_form.html", {"form": form})
