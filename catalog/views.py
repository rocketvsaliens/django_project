import re

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Contact, Version


def is_valid_version(version):
    pattern = r'^\d{1,2}\.\d{1,2}\.\d{1,2}$'
    return re.match(pattern, version) is not None


class ProductListView(ListView):
    paginate_by = 5
    model = Product
    template_name = 'catalog/index.html'
    ordering = ['-pk']

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
        context['version'] = Version.objects.filter(product=self.kwargs['pk'], is_actual=True).order_by('-pk')
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание товара'
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST)
        else:
            context['formset'] = VersionFormset()
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object
            for f in formset:
                num = f.cleaned_data.get('number')
                if num and not is_valid_version(num):
                    form.add_error(None, "Версия должна быть формата Х.Х.Х или ХХ.ХХ.ХХ")
                    return self.form_invalid(form=form)
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:item', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        if not self.request.user.is_superuser and self.request.user.has_perm('catalog.set_published'):
            return ModeratorProductForm
        return ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение товара'
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
            if self.request.method == 'POST':
                context['formset'] = VersionFormset(self.request.POST, instance=self.object)
            else:
                context['formset'] = VersionFormset(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data().get('formset')

        if formset.is_valid():
            actual_version_count = 0
            for f in formset:
                num = f.cleaned_data.get('number')
                if num and not is_valid_version(num):
                    form.add_error(None, "Версия должна быть формата Х.Х.Х или ХХ.ХХ.ХХ")
                    return self.form_invalid(form=form)

                if f.cleaned_data.get('is_actual'):
                    actual_version_count += 1
                    if actual_version_count > 1:
                        form.add_error(None, "Вы можете выбрать только одну активную версию")
                        return self.form_invalid(form=form)

            formset.save()
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return (obj.owner == self.request.user
                or self.request.user.has_perms(['catalog.change_product'])
                or self.request.user.is_superuser)

    def handle_no_permission(self):
        raise Http404('У вас нет прав для изменения этого товара')


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.delete_product'


class ContactListView(ListView):
    model = Contact
    template_name = 'catalog/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context
