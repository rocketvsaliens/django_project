from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (ProductListView, ProductDetailView, ProductCreateView,
                           ProductUpdateView, ProductDeleteView, ContactListView, CategoriyListView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('item/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='item'),
    path('create_item/', ProductCreateView.as_view(), name='item_create'),
    path('update_item/<int:pk>/', ProductUpdateView.as_view(), name='item_update'),
    path('delete_item/<int:pk>/', ProductDeleteView.as_view(), name='item_delete'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('categories/', CategoriyListView.as_view(), name='categories'),
]
