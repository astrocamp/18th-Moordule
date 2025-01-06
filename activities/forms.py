from django import forms
from django.utils import timezone

from .models import Activity, Category


class ActivityForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="選擇興趣",
        required=True,
        error_messages={"required": "必須選擇一個類別！"},
    )

    class Meta:
        model = Activity
        fields = [
            "title",
            "description",
            "address",
            "start_time",
            "duration",
            "max_participants",
            "category",
        ]

    def clean_start_time(self):
        start_time = self.cleaned_data.get("start_time")
        if start_time and start_time < timezone.now():
            raise forms.ValidationError("聚會開始時間必須晚於當前時間！")
        return start_time


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "order"]
