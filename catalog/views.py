from django.views.generic import ListView, DetailView
from catalog.models import Product, Contact


class ProductListView(ListView):
    paginate_by = 5
    model = Product
    template_name = 'catalog/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['object'])
        return context


class ContactListView(ListView):
    model = Contact
    template_name = 'catalog/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context
