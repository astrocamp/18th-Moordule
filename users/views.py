from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django_htmx.middleware import HtmxDetails

from activities.models import Activity as Meetup

from .forms import UserRegistrationForm
from .models import CustomUser, Record


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# @login_required
# @require_GET
# def chat_room(request: HtmxHttpRequest, meetup_id):
#     print(meetup_id)

#     meetup = get_object_or_404(Meetup, id=meetup_id)
#     group_name = f"chat_meetup_{meetup_id}"

#     context = {
#         "meetup": meetup,
#         "group_name": group_name,
#         "room_name": f"meetup_{meetup_id}",
#     }
#     return render(request, "users/components/chat_room.html", context)


# Create your views here.


def test_view(request: HtmxHttpRequest):
    return render(request, "users/test.html")


def meetup_create_view(request: HttpRequest):
    return render(request, "users/meetup_create.html")


def upload_view(request: HttpRequest):
    if request.method == "POST":
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
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            signin_url = reverse("users:signin")
            return HttpResponse("", headers={"HX-Redirect": signin_url})

    meetups = Meetup.objects.filter(
        start_time__gte=timezone.now()  # 只抓還沒開始的活動
    ).order_by("start_time")[:2]

    return render(request, "users/signup.html", {"meetups": meetups})


def signin_view(request: HttpRequest):

    meetups = Meetup.objects.filter(
        start_time__gte=timezone.now()  # 只抓還沒開始的活動
    ).order_by("start_time")[:2]
    return render(request, "users/signin.html", {"meetups": meetups})


def user_create_view(request: HtmxHttpRequest):

    if request.POST:
        form = UserRegistrationForm(request.POST)
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
        dashboard_url = reverse("users:dashboard")
        return HttpResponse("", headers={"HX-Redirect": dashboard_url})

    return render(
        request,
        "users/components/signin_form.html",
        {
            "form": {
                "errors": ["電子郵件或密碼錯誤"],
                "data": {"email": email},  # 保留用戶輸入的 email
            },
        },
    )


def clear_errors(request):
    return HttpResponse("")


@login_required(redirect_field_name="")
def dashboard_view(request: HttpRequest):
    user = get_object_or_404(CustomUser, id=request.user.pk)

    return render(request, "users/dashboard.html", {"user": user})


def records_tag(request: HtmxHttpRequest, tag):
    if not request.htmx:
        return HttpResponse(status=400)

    records = Record.objects.filter(user_id=request.user.pk, type=tag).order_by(
        "-created_at"
    )
    print(records)
    paginator = Paginator(records, 5)
    page = request.GET.get("page", 1)
    page_object = paginator.get_page(page)
    extra_rows = 5 - len(page_object.object_list)
    context = {"records": page_object, "extra_rows": range(extra_rows)}
    return render(request, "users/components/records.html", context)


def topup_records_tag(request):
    return render(request, "users/components/records.html")
