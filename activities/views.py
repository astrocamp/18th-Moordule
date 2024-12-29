from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import ActivityForm, CategoryForm
from .models import Activity, Category, MeetupPaticipat
from django.db.models import Q


# 檢查活動的擁有者是否為當前用戶
def get_activity_for_user(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if activity.owner != request.user:
        raise PermissionDenied("您無權執行此操作！")
    return activity

def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)





def activities(request):
    index = Activity.objects.all()
    category_id = request.GET.get("category")
    if category_id:
        index = index.filter(category_id=category_id)

    return render(request, 'activities/index.html', {'activities': index})




@login_required
def create(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.owner = request.user  # 綁定當前用戶
            activity.save()
            return redirect("activities:events")
        else:
            return render(request,"activities/create.html", {"form": form,  "categories": categories})
    else:
        form = ActivityForm()
    return render(request, "activities/create.html",{
        "form": form,
        "categories": categories,
         "form_data": form.cleaned_data if form.is_bound else None,
        })




def created_events(request):
    # 只顯示使用者建立的活動
    events = Activity.objects.all()
    return render(request, 'activities/created_events.html', {'activities': events})




@login_required
# @user_passes_test(ambda user: user.is_superuser)
# 目前超級使用者功能未完全,之後要管理者才能進入
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("activities:category")
    else:
        form = CategoryForm()
        
    categories = Category.objects.all()
    return render(request,"activities/create_category.html", {"form": form, "categories": categories})

@login_required
# @user_passes_test(ambda user: user.is_superuser)
# 目前超級使用者功能未完全,之後要管理者才能進入
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return redirect("activities:category") 
    except Category.DoesNotExist:
        return redirect("activities:category")  



@login_required
def update(request, activity_id):
    categories = Category.objects.all()
    activity = get_object_or_404(Activity, id=activity_id)
    if activity.owner != request.user:
        raise PermissionDenied("您無權編輯此活動！")
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("activities:index")
        else:
            print(form.errors)  
            return render(request, "activities/update.html", {
                "form": form,
                "activity": activity,
                "categories": categories,
                "error_message": "更新失敗，請檢查表單資料。",
                }) 
    else:
        form = ActivityForm(instance=activity)      
    return render(request, "activities/update.html", {
        "form": form, 
        "activity": activity,
        "categories": categories,
        })



@login_required
def delete(request, activity_id):
    activity = get_activity_for_user(request, activity_id)
    activity.delete()
    return redirect("activities:events")


@login_required
def confirm_delete(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if activity.owner != request.user:
        raise PermissionDenied("您無權刪除此活動！")
    if request.method == "POST":
        activity.delete()
        return redirect("activities:events")
    return render(request, "activities/confirm_delete.html", {"activity": activity})


@login_required
def join_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    # 檢查活動是否已經滿員
    if activity.participants.count() >= activity.max_participants:
        return render(request, "activities/detail.html", {
            "activity": activity, 
            "error_message": "人數已滿！"
            })
    # 如果用戶未參加過該活動，則加入活動
    participation, created = MeetupPaticipat.objects.get_or_create(activity=activity, participant=request.user)

    if created:
        message = "您已成功參加活動！"
    else:
        message = "您已經參加過此活動！"

        return redirect("activities:index")


def search(request):
    activities = Activity.objects.all()
    if request.method == "POST":  # 確保處理 POST 請求
        keyword = request.POST.get("keyword", "").strip()  # 去除多餘的空白
        if keyword:
            # 使用 Q 查詢條件比對所有欄位
            activities = activities.filter(
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(address__icontains=keyword)
            )
        return render(request,"activities/search.html",
            {"activities": activities, "keyword": keyword},
        )
    return render(request, "activities/search.html", {"activities": activities})

def information(request):
    return render(request,"activities/information.html")