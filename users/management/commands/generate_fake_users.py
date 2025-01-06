from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = "生成假用戶資料"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10, help="要生成的用戶數量(預設: 10)")
        parser.add_argument(
            "--force",
            action="store_true",
            help="強制重新生成（會刪除現有非管理員用戶）",
        )

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        force = kwargs["force"]
        fake = Faker()  # 改用英文版本

        # 如果是強制模式，先刪除現有非管理員用戶
        if force:
            deleted_count = User.objects.filter(is_superuser=False).delete()[0]
            self.stdout.write(f"已刪除 {deleted_count} 個現有用戶")

        # 批次創建用戶
        users = []
        try:
            with transaction.atomic():
                for i in range(count):
                    username = fake.user_name()

                    # 確保用戶名唯一
                    suffix = 1
                    temp_username = username
                    while User.objects.filter(username=temp_username).exists():
                        temp_username = f"{username}{suffix}"
                        suffix += 1
                    username = temp_username

                    user = User(
                        username=username,
                        email=f"{username}@example.com",
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                    )
                    user.set_password("password123")  # 設置默認密碼
                    users.append(user)
                    self.stdout.write(f"準備第 {i+1} 個用戶: {username}")

                # 批次創建
                created_users = User.objects.bulk_create(users)

                self.stdout.write(self.style.SUCCESS(f"成功創建 {len(created_users)} 個用戶"))

                # 列出創建的用戶資訊
                self.stdout.write("\n創建的用戶列表:")
                for user in created_users:
                    self.stdout.write(
                        f"用戶名: {user.username}, "
                        f"Email: {user.email}, "
                        f"姓名: {user.get_full_name()}, "
                        f"密碼: password123"
                    )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"創建用戶時發生錯誤: {str(e)}"))
