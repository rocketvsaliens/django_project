from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_cache_for_categories(category):

    if CACHE_ENABLED:
        key = f'categories_list'
        categories_list = cache.get(key)
        if categories_list is None:
            categories_list = category.objects.all()
            cache.set(key, categories_list)
    else:
        categories_list = category.objects.all()
    return categories_list
