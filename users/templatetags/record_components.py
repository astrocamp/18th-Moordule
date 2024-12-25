from decimal import Decimal

from django import template
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Sum

from users.models import Record

register = template.Library()


@register.inclusion_tag("users/components/stats_field.html")
def stats_field(*, label, value):
    return {"label": label, "value": value}


@register.inclusion_tag("users/components/member_statistics.html")
def member_statistics(id, type):
    # 使用聚合查詢進行統計
    stats = Record.objects.filter(user_id=id, type=type).aggregate(
        count=Count("id"), total_amount=Sum("amount"), average=Avg("amount")
    )

    # 確保沒有資料時返回 0
    stats = {
        "count": stats["count"] or 0,
        "total_amount": stats["total_amount"] or Decimal("0.00"),
        "average": (
            stats["average"].quantize(Decimal("0.01"))
            if stats["average"]
            else Decimal("0.00")
        ),
    }

    meetup_labels = ["參與次數", "總金額", "平均每次"]
    topup_labels = ["儲值次數", "總儲值", "平均每次"]

    return {
        "stats": stats,
        "labels": meetup_labels if type == "meetup" else topup_labels,
    }


@register.inclusion_tag("users/components/record_manager.html", takes_context=True)
def record_manager(context, type):

    request = context["request"]

    if "page" not in request.GET:
        return {"should_render": False}

    # 查詢記錄，包括 notes 資訊
    records = Record.objects.filter(user_id=request.user.pk, type=type).order_by(
        "-created_at"
    )
    ITEMS_PER_PAGE = 5
    paginator = Paginator(records, ITEMS_PER_PAGE)
    page = request.GET.get("page")

    try:
        page = int(page)
        if page < 1 or page > paginator.num_pages:
            return {
                "type": type,
                "user": request.user,
                "should_render": True,
                "should_redirect": True,
                "redirect_page": 1 if page < 1 else paginator.num_pages,
            }

        page_object = paginator.get_page(page)
        extra_rows = 5 - len(page_object.object_list)
        return {
            "type": type,
            "user": request.user,
            "should_render": True,
            "should_redirect": False,
            "page_object": page_object,
            "paginator": paginator,
            "extra_rows": range(extra_rows),
        }

    except ValueError:
        return {
            "type": type,
            "user": request.user,
            "should_render": True,
            "should_redirect": True,
            "redirect_page": 1,
        }
