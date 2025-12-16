from django.conf import settings
from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """
    Возвращает список продуктов по id категории.
    Использует низкоуровневое кеширование.
    """
    # Если кеш выключен - просто берем из БД
    if not settings.CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id)

    # Формируем уникальный ключ для кеша
    key = f'products_category_{category_id}'

    # Пытаемся получить данные из кеша
    products = cache.get(key)

    # Если данных нет в кеше - берем из БД и записываем в кеш
    if products is None:
        products = Product.objects.filter(category_id=category_id)
        cache.set(key, products, timeout=60 * 10)  # Кеш на 10 минут

    return products