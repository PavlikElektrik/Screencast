from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы пользователей и назначает права'

    def handle(self, *args, **options):
        # 1. Создаем группу "Модераторы"
        moderator_group, created = Group.objects.get_or_create(name='Модераторы')

        # 2. Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # 3. Находим нужные права (Permissions)
        # Право на удаление продуктов (стандартное Django право)
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        # Право на отмену публикации (наше кастомное право)
        unpublish_permission = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )

        # 4. Добавляем права группе
        moderator_group.permissions.add(delete_permission)
        moderator_group.permissions.add(unpublish_permission)

        self.stdout.write(self.style.SUCCESS(f'Группа "Модераторы" успешно настроена!'))