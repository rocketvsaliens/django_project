from django.contrib import admin
from catalog.models import Category, Product, Contact, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class VersionInline(admin.StackedInline):
    model = Version
    extra = 1
    can_delete = False
    verbose_name = 'версия'
    verbose_name_plural = 'версии'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    inlines = [
        VersionInline,
    ]


# @admin.register(Version)
# class VersionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'number', 'title', 'is_actual')
#     list_filter = ('product',)
#     search_fields = ('number', 'title')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')
