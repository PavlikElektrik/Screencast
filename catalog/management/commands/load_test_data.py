from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Загружает тестовые данные из фикстур"

    def handle(self, *args, **options):
        # Удаляем старые данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем фикстуры
        call_command('loaddata', 'categories.json', verbosity=0)
        call_command('loaddata', 'products.json', verbosity=0)

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно загружены!')
        )