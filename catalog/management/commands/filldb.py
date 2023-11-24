from django.core.management import BaseCommand
from catalog.models import Product, Category, Contact


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        categories_list = [
            {'name': 'Роботы', 'description': 'Izhevsk Dynamics'},
            {'name': 'Голограммы', 'description': 'Ivanovo Holograms'},
            {'name': 'Протезы и экзоскелеты', 'description': 'Tomsk Technologies'},
        ]

        cat1 = categories_list[0].get('name')
        cat2 = categories_list[1].get('name')
        cat3 = categories_list[2].get('name')

        product_list = [
            {'name': 'Ваня', 'description': 'Робот-пылесос', 'category': cat1, 'price': '0'},
            {'name': 'Глаша', 'description': 'Робот-доярка', 'category': cat1, 'price': '10000'},
            {'name': 'Гошик', 'description': 'Робот-массажист', 'category': cat1, 'price': '10000'},
            {'name': 'Галя', 'description': 'Голограмма жены по подписке', 'category': cat2, 'price': '100500'},
            {'name': 'Роборука', 'description': 'Ворованная', 'category': cat3, 'price': '100'}
        ]

        for category_item in categories_list:
            Category.objects.create(**category_item)

        products_for_create = []
        for product_item in product_list:
            category = product_item.pop('category')
            category = Category.objects.get(name=category)
            product_item['category'] = category
            products_for_create.append(
                Product(**product_item)
            )

        Product.objects.bulk_create(products_for_create)
