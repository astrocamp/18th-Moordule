from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=15, help_text="分類名稱")
    description = models.TextField(help_text="分類描述", blank=True, null=True)
    order = models.PositiveIntegerField(help_text="排序", default=0)

    def __str__(self):
        return self.name


class Activity(models.Model):
    title = models.CharField(max_length=15, help_text="聚會標題")
    description = models.TextField(help_text="聚會描述", blank=True)
    address = models.CharField(
        max_length=255, help_text="聚會地址，例：台北市信義區市府路1號"
    )
    start_time = models.DateTimeField(help_text="聚會開始時間")
    duration = models.PositiveIntegerField(
        help_text="預估聚會持續時間（小時）", default=1
    )
    max_participants = models.PositiveIntegerField(help_text="參加人數上限", default=4)
    created_at = models.DateTimeField(auto_now_add=True, help_text="聚會建立時間")
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="聚會分類",
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="created_activities",
        help_text="聚會建立者",
    )
    photo = models.ImageField(
        upload_to="activities_photo",
        null=True,
        blank=True,
    )
    STATUS_CHOICES = [
        ("pending", "待審核"),
        ("approved", "已通過"),
        ("rejected", "已拒絕"),
        ("expired", "已過期"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", help_text="聚會狀態"
    )
    is_approved = models.BooleanField(default=False, help_text="活動是否已審核通過")

    rejection_reason = models.CharField(
        max_length=255, null=True, blank=True, help_text="活動拒絕原因"
    )

    @property
    def end_time(self):
        return self.start_time + timedelta(hours=self.duration)

    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

    @property
    def is_upcoming(self):
        return self.start_time > timezone.now()

    @property
    def is_finished(self):
        return self.end_time < timezone.now()

    def save(self, *args, **kwargs):
        # 根據活動的結束時間自動設置狀態
        if self.end_time < timezone.now():
            self.status = "expired"
        super().save(*args, **kwargs)


class MeetupPaticipat(models.Model):
    activity = models.ForeignKey(
        "Activity",
        on_delete=models.CASCADE,
        related_name="participants",
        help_text="聚會",
    )
    participant = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="meetups", help_text="參與者"
    )
    joined_at = models.DateTimeField(auto_now_add=True, help_text="加入時間")

    class Meta:
        unique_together = ("activity", "participant")

    def __str__(self):
        return f"{self.activity.title} - {self.participant.username}（{self.joined_at.strftime('%Y-%m-%d %H:%M')})"


class ActivityApproval(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="approvals",
        help_text="被審核的活動",
    )
    reviewer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, help_text="審核者"
    )
    approved = models.BooleanField(default=False, help_text="是否審核通過")
    comment = models.TextField(blank=True, null=True, help_text="審核意見")
    created_at = models.DateTimeField(auto_now_add=True, help_text="審核時間")

    def __str__(self):
        return f"{self.activity.title} - {self.reviewer.username}({'Approved' if self.approved else 'Rejected'})"
