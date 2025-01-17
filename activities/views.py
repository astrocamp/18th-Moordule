from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from moordule import settings
from .forms import ActivityForm, CategoryForm
from .models import Activity, Category, MeetupPaticipat
from django.http import HttpResponseForbidden
from datetime import date
from datetime import timedelta
from django.db import transaction
from cashflows.models import Wallet

def is_adult(birth_date):
    # 計算年齡，並檢查是否已滿18歲
    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age >= 18


def get_activity_for_user(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if activity.owner != request.user:
        raise PermissionDenied("您無權執行此操作！")
    return activity


def activities(request):
    categories = Category.objects.prefetch_related("activity_set")

    now = timezone.now()
    activities_by_category = {
        category: category.activity_set.filter(
            start_time__gte=now, status="approved"
        ).order_by("start_time")[:4]
        for category in categories
    }

    return render(
        request,
        "activities/index.html",
        {
            "activities_by_category": activities_by_category,
            "categories": categories,
        },
    )


@login_required
def create(request):
    # 檢查用戶是否填寫了個人資料
    if (
        not request.user.username
        or not request.user.birth_date
        or not request.user.live_in
        or not request.user.bio
    ):
        messages.error(request, "請先填寫您'必填＊'的個人資料才能創建聚會")
        return redirect(
            "users:user_page", tag="account"
        )  # 重定向到編輯頁面方便編輯寫入

    # 檢查用戶是否年滿 18 歲
    if not is_adult(request.user.birth_date):
        messages.error(request, "您必須年滿 18 歲才能創建聚會。")
        return redirect("users:user_page", tag="member")  # 如果未滿 18 歲，導至個人頁面

    categories = Category.objects.all()
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(user=request.user)

                cteare_cost = 1
                if wallet.create_activity < cteare_cost:
                    messages.error(request, "餘額不足，請先充值！")
                    return redirect("cashflows:index")

                wallet.create_activity -= cteare_cost
                wallet.save()
                  
            activity = form.save(commit=False)
            if activity.start_time < timezone.now():
                messages.error(request, "聚會開始時間必須晚於當前時間！")
                return render(
                    request,
                    "activities/create.html",
                    {"form": form, "categories": categories},
                )

            activity.owner = request.user
            activity.save()
            messages.success(request, "創建聚會，並扣款成功。")
            return redirect("users:user_page", tag="my_activities")

        else:
            return render(
                request,
                "activities/create.html",
                {"form": form, "categories": categories},
            )
    else:
        form = ActivityForm()
    return render(
        request,
        "activities/create.html",
        {
            "form": form,
            "categories": categories,
            "form_data": form.cleaned_data if form.is_bound else None,
        },
    )


@login_required
def created_activities(request):
    activities = Activity.objects.filter(owner=request.user)
    return render(request, "activities/my_activities.html", {"activities": activities})


@login_required
@staff_member_required
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("activities:category")
    else:
        form = CategoryForm()

    categories = Category.objects.all()
    return render(
        request,
        "activities/create_category.html",
        {"form": form, "categories": categories},
    )


@login_required
@staff_member_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if not request.user.is_staff:
        raise PermissionDenied("您無權執行此操作！")
    category.delete()
    return redirect("activities:category")


@login_required
def update(request, activity_id):
    categories = Category.objects.all()
    activity = get_activity_for_user(request, activity_id)

    if activity.status == "approved" and not request.user.is_superuser:
        return HttpResponseForbidden("只有平台管理者可以修改已批准的活動。")

    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("users:user_page", tag="my_activities")
        else:
            print(form.errors)
            return render(
                request,
                "activities/update.html",
                {
                    "form": form,
                    "activity": activity,
                    "categories": categories,
                    "error_message": "更新失敗，請檢查表單資料。",
                },
            )
    else:
        form = ActivityForm(instance=activity)
    return render(
        request,
        "activities/update.html",
        {
            "form": form,
            "activity": activity,
            "categories": categories,
        },
    )


@login_required
def delete(request, activity_id):
    activity = get_activity_for_user(request, activity_id)
    activity.delete()
    return redirect("activities:index")


@login_required
def confirm_delete(request, activity_id):
    activity = get_activity_for_user(request, activity_id)
    if request.method == "POST":
        wallet = Wallet.objects.get(user=request.user)

        create_cost = 1  
        with transaction.atomic():
            # 扣除錢包餘額
            wallet.create_activity += create_cost
            wallet.save()


            activity.delete()
        return redirect("users:user_page", tag="my_activities")
    return render(request, "activities/confirm_delete.html", {"activity": activity})


def join_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    # 在用戶點擊按鈕時檢查是否滿 18 歲並且資料是否完整
    if (
        not request.user.username
        or not request.user.birth_date
        or not request.user.live_in
        or not request.user.bio
    ):
        messages.error(request, "請先填寫您必填＊的個人資料讓大家更了解您")
        return redirect(
            "users:user_page", tag="account"
        )  # 如果資料不完整，重定向到個人資料頁面

    # 檢查用戶是否年滿 18 歲
    if not is_adult(request.user.birth_date):
        messages.error(request, "您必須年滿 18 歲才能參加聚會。")
        return redirect(
            "users:user_page", tag="member"
        )  # 如果未滿 18 歲，重定向至個人資料頁面

    if activity.status != "approved":
        return render(
            request,
            "activities/information.html",
            {
                "activity": activity,
                "error_message": "此活動尚未審核通過，無法參加！",
                "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
            },
        )

    is_participating = activity.participants.filter(id=request.user.id).exists()
    message = None
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY

    if request.method == "POST":
        if "join" in request.POST:
            if activity.participants.count() >= activity.max_participants:
                messages.error(request, "目前聚會人數已滿！")
                return render(
                    request,
                    "activities/information.html",
                    {
                        "activity": activity,
                        "message": message,
                        "google_maps_api_key": google_maps_api_key,
                    },
                )
            
           
            wallet = Wallet.objects.get(user=request.user)

            activity_cost = 1  
            if wallet.join_activity < activity_cost:
                messages.error(request, "餘額不足，請先充值！")
                return redirect("cashflows:index")  

            # 使用交易保證扣款和參加活動的一致性
            with transaction.atomic():
                wallet.join_activity -= activity_cost
                wallet.save()

           
            participation, created = MeetupPaticipat.objects.get_or_create(
                activity=activity, participant=request.user
            )
            messages.success(
                request, "您已成功報名聚會，系統已自動扣款！" if created else "您已經報名此聚會！"
            )

    return render(
        request,
        "activities/information.html",
        {
            "activity": activity,
            "is_participating": is_participating,
            "google_maps_api_key": google_maps_api_key,
        },
    )


def leave_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    participation = MeetupPaticipat.objects.filter(
        activity=activity, participant=request.user
    ).first()
    if request.method == "POST":
        if participation:
            participation.delete()

            wallet = Wallet.objects.get(user=request.user)

            activity_cost = 1  
            with transaction.atomic():
                wallet.join_activity += activity_cost
                wallet.save()

            messages.success(request, "您已成功退出聚會！")
        else:
            messages.error(request, "您未參加此聚會，無法退出！")

        return redirect("users:user_page", tag="activities")

    return render(
        request,
        "activities/leave_information.html",
        {
            "activity": activity,
            "participation": participation,
            "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        },
    )


def search(request):
    activities = Activity.objects.filter(status="approved")  # 只顯示已審核的活動
    if request.method == "POST":
        keyword = request.POST.get("keyword", "").strip()
        if keyword:
            activities = activities.filter(
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(address__icontains=keyword)
            )
        return render(
            request,
            "activities/search.html",
            {"activities": activities, "keyword": keyword},
        )
    return render(request, "activities/search.html", {"activities": activities})


def today(request):
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)

    todays_events = Activity.objects.filter(
        start_time__date__in=[today, tomorrow], status="approved"
    ).order_by("start_time")

    activities_by_today = {}
    activities_per_page = 8

    page_number = request.GET.get(f"page", 1)

    paginator = Paginator(todays_events, activities_per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    activities_by_today[activities] = page_obj

    return render(
        request,
        "activities/today.html",
        {
            "todays_events": page_obj,
        },
    )


def render_activities(request, template_name):
    categories = Category.objects.prefetch_related("activity_set")
    now = timezone.now()
    activities_by_category = {}
    activities_per_page = 8

    for category in categories:
        activities = category.activity_set.filter(
            start_time__gte=now, status="approved"
        ).order_by("start_time")
        page_number = request.GET.get(f"page_{category.id}", 1)
        paginator = Paginator(activities, activities_per_page)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        activities_by_category[category] = page_obj

    return render(
        request,
        template_name,
        {
            "activities_by_category": activities_by_category,
            "categories": categories,
        },
    )


def eating(request):
    return render_activities(request, "activities/eating.html")


def driking(request):
    return render_activities(request, "activities/driking.html")


def sports(request):
    return render_activities(request, "activities/sports.html")


def singing(request):
    return render_activities(request, "activities/singing.html")


def movies(request):
    return render_activities(request, "activities/movies.html")


def discussion(request):
    return render_activities(request, "activities/discussion.html")


@login_required
def view_activity_participants(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    # 確保只有活動的創建者才能查看參與者資料
    if activity.owner != request.user:
        raise PermissionDenied("您無權查看此活動的參與者！")

    participants = activity.participants.all()

    participants_info = [
        {
            "username": participant.participant.username,  # 使用 participant.participant 存取 username
            "avatar": (
                participant.participant.avatar.url
                if participant.participant.avatar
                else None
            ),
            "bio": (
                participant.participant.bio
                if participant.participant.bio
                else "無自我介紹"
            ),
            "age": (
                participant.participant.birth_date
                and (timezone.now().date() - participant.participant.birth_date).days
                // 365
                if participant.participant.birth_date
                else "未知"
            ),
            "gender": (
                participant.participant.get_gender_display()
                if participant.participant.gender
                else "未知"
            ),
            "live_in": (
                participant.participant.get_live_in_display()
                if participant.participant.live_in
                else "未知"
            ),
        }
        for participant in participants
    ]

    return render(
        request,
        "activities/participants.html",
        {"activity": activity, "participants_info": participants_info},
    )
