from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import ActivityForm, CategoryForm
from .models import Activity, Category, MeetupPaticipat
from django.utils import timezone
from django.db.models import Q


def get_activity_for_user(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if activity.owner != request.user:
        raise PermissionDenied("您無權執行此操作！")
    return activity


def activities(request):
    categories = Category.objects.prefetch_related("activity_set")

    now = timezone.now()  # 過濾掉過期的活動，只顯示未過期的活動
    activities_by_category = {
        category: category.activity_set.filter(start_time__gte=now).order_by(
            "start_time"
        )[:4]
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
    categories = Category.objects.all()
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.owner = request.user
            activity.save()
            return redirect("activities:my_activities")
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

    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("activities:index")
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
        activity.delete()
        return redirect("activities:my_activities")
    return render(request, "activities/confirm_delete.html", {"activity": activity})


def join_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    is_participating = activity.participants.filter(id=request.user.id).exists()
    message = None

    if request.method == "POST":
        if "join" in request.POST:
            if activity.participants.count() >= activity.max_participants:
                return render(
                    request,
                    "activities/information.html",
                    {
                        "activity": activity,
                        "error_message": "聚會人數已滿！",
                    },
                )

            participation, created = MeetupPaticipat.objects.get_or_create(
                activity=activity, participant=request.user
            )
            message = "您已成功報名聚會！" if created else "您已經報名此聚會！"

        elif "leave" in request.POST:
            participation = MeetupPaticipat.objects.filter(
                activity=activity, participant=request.user
            ).first()
            if participation:
                participation.delete()
                message = "您已成功退出聚會！"
            else:
                message = "您未參加此聚會，無法退出！"

        return render(
            request,
            "activities/information.html",
            {
                "activity": activity,
                "message": message,
                "is_participating": is_participating,
            },
        )

    return render(
        request,
        "activities/information.html",
        {
            "activity": activity,
            "is_participating": is_participating,
        },
    )


def search(request):
    activities = Activity.objects.all()
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
