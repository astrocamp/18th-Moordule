from django.contrib import admin
from .models import Activity, ActivityApproval
from django.contrib import messages
from django.db.models import Count
from django.utils.html import format_html


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "get_status_display", "is_approved")
    list_filter = ("status", "is_approved")
    actions = ["approve_activity", "reject_activity", "expire_activity"]

    def get_status_display(self, obj):
        if obj.status == "pending":
            return format_html('<span style="color:orange;">{}</span>', "待審核")
        elif obj.status == "approved":
            return format_html('<span style="color:green;">{}</span>', "已通過")
        elif obj.status == "rejected":
            return format_html('<span style="color:red;">{}</span>', "已拒絕")
        elif obj.status == "expired":
            return format_html('<span style="color:gray;">{}</span>', "已過期")
        return obj.status

    get_status_display.short_description = "狀態"

    # 批量批准活動
    def approve_activity(self, request, queryset):
        queryset.update(status="approved", is_approved=True)
        # 創建或更新 ActivityApproval 審核記錄
        for activity in queryset:
            ActivityApproval.objects.create(
                activity=activity,
                reviewer=request.user,  # 審核者為當前用戶
                approved=True,
            )
        messages.success(request, "選中的活動已批准。")

    approve_activity.short_description = "批准選中活動"

    # 批量拒絕活動
    def reject_activity(self, request, queryset):
        queryset.update(status="rejected", is_approved=False)
        # 創建或更新 ActivityApproval 審核記錄
        for activity in queryset:
            ActivityApproval.objects.create(
                activity=activity,
                reviewer=request.user,  # 審核者為當前用戶
                approved=False,
            )
        messages.success(request, "選中的活動已拒絕。")

    reject_activity.short_description = "拒絕選中活動"

    # 批量設為過期
    def expire_activity(self, request, queryset):
        queryset.update(status="expired")
        messages.success(request, "選中的活動已設為過期。")

    expire_activity.short_description = "設為過期"

    @staticmethod
    def get_activity_approval_statistics():
        statistics = Activity.objects.values("status").annotate(count=Count("status"))
        return statistics

    def changelist_view(self, request, extra_context=None):
        approval_stats = self.get_activity_approval_statistics()
        extra_context = extra_context or {}
        extra_context["approval_stats"] = approval_stats
        return super().changelist_view(request, extra_context=extra_context)
