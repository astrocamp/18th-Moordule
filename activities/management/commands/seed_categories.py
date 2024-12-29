# your_app/management/commands/seed_categories.py
from django.core.management.base import BaseCommand
from activities.models  import Category

class Command(BaseCommand):
    help = "Seeds the database with categories"

    def handle(self, *args, **options):
        initial_categories = [
            {"name": "揪吃飯", "description": "享用美食揪起來", "order": 1},
            {"name": "揪唱歌", "description": "一起歡唱揪開心", "order": 2},
            {"name": "揪喝酒", "description": "微醺看世界揪好喝", "order": 3},
            {"name": "揪運動", "description": "一起動動揪健康", "order": 4},
            {"name": "揪電影", "description": "電影賞析揪美好", "order": 5},
            {"name": "揪討論", "description": "專業討論揪給力", "order": 6},
        ]

        for category_data in initial_categories:
            category, created = Category.objects.get_or_create(
                name=category_data["name"],
                description=category_data["description"],
                order=category_data["order"]
            )

            # 輸出結果，告訴我們是創建了新分類還是已經存在
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category '{category.name}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"Category '{category.name}' already exists"))


# 請執行python manage.py seed_categories 來執行這個命令Makefile有設定seed