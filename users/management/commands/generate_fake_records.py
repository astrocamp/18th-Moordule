import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from users.models import Record

User = get_user_model()


class Command(BaseCommand):
    help = "產生假紀錄資料"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, help="每個用戶要創建的紀錄數量")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        fake = Faker(["zh_TW"])

        # 取得所有用戶
        users = User.objects.all()

        if not users.exists():
            self.stdout.write(
                self.style.ERROR("No users found. Please create users first.")
            )
            return

        for user in users:
            for _ in range(count):
                record_type = random.choice(
                    [choice[0] for choice in Record.TYPE_CHOICES]
                )

                # 根據不同類型產生不同的 notes 和 amount
                if record_type == "meetup":
                    amount = Decimal(random.randint(-1000, -100))
                    notes = {
                        "meetup_title": fake.text(max_nb_chars=20),
                        "location": fake.address(),
                        "participants": random.randint(2, 10),
                    }
                else:  # topup
                    amount = Decimal(random.randint(100, 2000))
                    notes = {
                        "payment_method": random.choice(["信用卡", "LINE Pay"]),
                        "transaction_id": fake.uuid4(),
                    }

                try:
                    Record.objects.create(
                        user=user, type=record_type, amount=amount, notes=notes
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created {record_type} record for user {user.email}: ${amount}"
                        )
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed to create record for user {user.email}: {str(e)}"
                        )
                    )
