from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, contacts, show_item

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('item/<int:product_pk>/', show_item, name='item')
]
