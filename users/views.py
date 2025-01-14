from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django_htmx.middleware import HtmxDetails
from django.contrib import messages
from activities.models import Activity as Meetup
from activities.models import MeetupPaticipat as MeetupParticipant
from cashflows.models import Payment
from django.shortcuts import redirect
from .decorators import anonymous_required
from .forms import AboutMeForm, CustomUserChangeForm, UserRegistrationForm
from django.contrib.auth.views import LogoutView


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# Create your views here.


@login_required
def password_view(request):
    return render(request, "users/components/password.html")


@login_required
def password_change_view(request):
    if request.method == "GET":
        return render(request, "users/components/password_change_form.html")

    user = request.user
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password1")
    confirm_password = request.POST.get("new_password2")

    if not user.check_password(old_password):
        return render(
            request,
            "users/components/password_change_form.html",
            {"error": {"code": 0, "message": "舊密碼輸入有誤"}},
        )

    if new_password != confirm_password:
        return render(
            request,
            "users/components/password_change_form.html",
            {"error": {"code": 1, "message": "密碼不一致"}},
        )

    user.set_password(new_password)
    user.password_changed_at = timezone.now()
    user.save()
    update_session_auth_hash(request, user)

    return render(request, "users/components/password.html", {"user": user})


@login_required
def user_page_view(request, tag="member"):
    user = request.user
    context = {"tag": tag}

    if tag == "member":
        context["meetup"] = (
            Meetup.objects.filter(
                start_time__gte=timezone.now(),
                id__in=MeetupParticipant.objects.filter(participant=user).values(
                    "activity_id"
                ),  # 透過參加者關聯查詢
            )
            .order_by("start_time")
            .first()
        )
    elif tag == "account":
        form = CustomUserChangeForm()
        context["form"] = form
    elif tag == "activities":
        meetups = (
            MeetupParticipant.objects.filter(
                participant=user, activity__start_time__gt=timezone.now()
            )
            .annotate(total_count=Count("activity__participants"))
            .order_by("activity__start_time")
        )
        context["meetups"] = meetups
    elif tag == "my_activities":
        activities = Meetup.objects.filter(owner=user)
        context["activities"] = activities

    elif tag == "wallet":
        # 從 Wallets 模型抓取使用者的錢包資訊
        wallet = Payment.objects.filter(user=user).first()
        if wallet:
            context["wallet_balance"] = wallet.amount
        else:
            context["wallet_balance"] = 0  

        # 從 Payments 模型抓取與使用者相關的交易紀錄
        transactions = Payment.objects.filter(order_id__startswith="WALLET").order_by("-created_at")
        context["transactions"] = transactions
        
        

    else:
        # 若沒有符合任何條件，保留基本的 context
        context = {"tag": tag}

    if not request.headers.get("HX-Request"):
        return render(request, "users/dashboard.html", context)

    return render(request, f"users/components/{tag}.html", context)


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


@anonymous_required
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


@anonymous_required
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
            messages.success(request, "註冊成功，請登入")
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
        messages.success(request, "登入成功")
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


@require_GET
def info_view(request: HtmxHttpRequest):

    print("hobbies:", request.user)
    print("get_hobbies_display:", request.user)
    messages.success(request, "個人資料更新成功")
    return render(request, "users/components/info.html")


def info_form_view(request: HtmxHttpRequest):
    messages.success(request, "個人資料更新成功")
    return render(request, "users/components/info_form.html")


@login_required
def info_edit_view(request: HtmxHttpRequest):
    user = request.user
    if request.method == "POST":

        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "個人資料更新成功")
            return render(request, "users/components/info.html", {"user": user})
        print(form.errors)
        return render(request, "users/components/info_form.html", {"form": form})

    # 處理 GET 請求
    form = CustomUserChangeForm(instance=user)
    return render(request, "users/components/info_form.html", {"form": form})


@require_GET
def about_me_view(request: HtmxHttpRequest):
    return render(request, "users/components/about_me.html")


@login_required
def about_me_edit_view(request: HtmxHttpRequest):
    user = request.user
    if request.method == "POST":
        form = AboutMeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "個人資料更新成功")
            return render(request, "users/components/about_me.html", {"user": user})
        return render(request, "users/components/about_me_form.html", {"form": form})

    form = AboutMeForm(instance=user)
    return render(request, "users/components/about_me_form.html", {"form": form})


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # 添加成功消息
        messages.success(request, "您已成功登出。")
        return super().dispatch(request, *args, **kwargs)
