from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.utils.timezone import now
from .models import Activity

def activities(request):
    index = Activity.objects.all()
    return render(request, 'activities/index.html', {'activities': index})



def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        address = request.POST.get("address")
        start_time = request.POST.get("start_time")
        duration = request.POST.get("duration", 1)
        max_participants = request.POST.get("max_participants", 10)
        
        
        if not title or not address or not start_time:
            error_message = "請確保標題、地址和開始時間為必填項目！"
            return render(request, "activities/create.html", {"error_message": error_message})

        
        Activity.objects.create(
            title=title,
            description=description,
            address=address,
            start_time=start_time,
            duration=duration,
            max_participants=max_participants
            
        )
        return redirect("activities:index")
    return render(request, "activities/create.html")




def update(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        address = request.POST.get("address", "").strip()
        start_time = request.POST.get("start_time")
        duration = request.POST.get("duration", 1)
        max_participants = request.POST.get("max_participants", 10)

    
        error_message = None
        if not title or not address or not start_time:
            error_message = "請確保標題、地址和開始時間為必填項目！"

        if error_message:
            return render(request, "activities/update.html", {
                "error_message": error_message,
                "activity": activity
            })

        
        activity.title = title
        activity.description = description
        activity.address = address
        activity.start_time = start_time
        activity.duration = int(duration)
        activity.max_participants = int(max_participants)
        activity.save()  

        return redirect("activities:index")  

    return render(request, "activities/update.html", {"activity": activity})


def delete(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    activity.delete()

    return redirect("activities:index")

def confirm_delete(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if request.method == "POST":
        activity.delete()
        return redirect("activities:index")
    return render(request, "activities/confirm_delete.html", {"activity": activity})

