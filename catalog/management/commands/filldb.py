from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories_list = [
            {'name': 'Роботы', 'description': 'Izhevsk Dynamics'},
            {'name': 'Голограммы', 'description': 'Ivanovo Holograms'},
            {'name': 'Протезы и экзоскелеты', 'description': 'Tomsk Technologies'},
        ]

        product_list = [
            {'name': 'Ваня', 'description': 'Робот-пылесос', 'category_id': 1, 'price': '0'},
            {'name': 'Глаша', 'description': 'Робот-доярка', 'category_id': 1, 'price': '10000'},
            {'name': 'Гошик', 'description': 'Робот-массажист', 'category_id': 1, 'price': '10000'},
            {'name': 'Галя', 'description': 'Голограмма жены по подписке', 'category_id': 2, 'price': '100500'},
            {'name': 'Роборука', 'description': 'Ворованная', 'category_id': 3, 'price': '100'}
        ]

        for category_item in categories_list:
            Category.objects.create(**category_item)

        products_for_create = []
        for product_item in product_list:
            category_id = product_item.pop('category_id')
            category = Category.objects.get(id=category_id)
            product_item['category'] = category
            products_for_create.append(
                Product(**product_item)
            )

        Product.objects.bulk_create(products_for_create)
