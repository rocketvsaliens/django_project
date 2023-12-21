from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contact, Version


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


class ProductCreateView(CreateView):
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
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:item', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение товара'
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
                if f.cleaned_data.get('is_actual'):
                    actual_version_count += 1
                    if actual_version_count > 1:
                        form.add_error(None, "Вы можете выбрать только одну активную версию")
                        return self.form_invalid(form=form)
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')


class ContactListView(ListView):
    model = Contact
    template_name = 'catalog/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context
