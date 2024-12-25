import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from activities.models import Activity as Meetups
from users.models import Record

User = get_user_model()


class Command(BaseCommand):
    help = "為用戶生成假記錄資料"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=20, help="每個用戶要生成的記錄數量(預設: 20)"
        )
        parser.add_argument(
            "--force", action="store_true", help="強制重新生成（會刪除現有記錄）"
        )

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        force = kwargs.get("force", False)
        faker = Faker("zh_TW")

        # 列出系統狀態
        users = User.objects.all()
        self.stdout.write(f"\n系統現況:")
        self.stdout.write(f"- 用戶總數: {users.count()}")
        self.stdout.write(f"- 記錄總數: {Record.objects.count()}")
        self.stdout.write(f"- 活動總數: {Meetups.objects.count()}")

        if not users.exists():
            self.stdout.write(
                self.style.ERROR(
                    "找不到任何用戶，請先執行 python manage.py generate_fake_users"
                )
            )
            return

        # 檢查每個用戶狀態
        for user in users:
            record_count = Record.objects.filter(user=user).count()
            self.stdout.write(
                f"用戶 {user.username} (ID: {user.pk}) 目前有 {record_count} 筆記錄"
            )

        # 如果是強制模式，刪除現有記錄
        if force:
            deleted_count = Record.objects.all().delete()[0]
            self.stdout.write(f"已刪除 {deleted_count} 筆現有記錄")

        meetup_topics = ["例行見面", "加時約會", "特別約會", "短約", "下午茶"]
        payment_methods = ["信用卡", "現金", "轉帳", "LINE Pay", "街口支付"]

        # 為每個用戶生成記錄
        total_records = []
        try:
            with transaction.atomic():
                for user in users:
                    records = []
                    for i in range(count):
                        is_meetup = random.choice([True, False])
                        date = timezone.now() - timedelta(
                            days=random.randint(0, 90),
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59),
                        )

                        if is_meetup:
                            record = Record(
                                user=user,
                                type="meetup",
                                amount=Decimal(random.randint(3000, 10000)),
                            )
                            record.set_notes(topic=random.choice(meetup_topics))
                        else:
                            record = Record(
                                user=user,
                                type="topup",
                                amount=Decimal(random.randint(10000, 50000)),
                            )
                            record.set_notes(
                                payment_method=random.choice(payment_methods)
                            )

                        record.created_at = date
                        records.append(record)

                    total_records.extend(records)
                    self.stdout.write(
                        f"已準備用戶 {user.username} 的 {len(records)} 筆記錄"
                    )

                # 批次創建所有記錄
                created_records = Record.objects.bulk_create(total_records)
                self.stdout.write(
                    self.style.SUCCESS(f"\n成功創建總計 {len(created_records)} 筆記錄")
                )

                # 更新每個用戶的記錄數統計
                self.stdout.write("\n最終記錄統計:")
                for user in users:
                    final_count = Record.objects.filter(user=user).count()
                    self.stdout.write(
                        f"用戶 {user.username} (ID: {user.pk}) 現有 {final_count} 筆記錄"
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"創建記錄時發生錯誤: {str(e)}"))
            return

        self.stdout.write(self.style.SUCCESS("記錄生成完成"))
