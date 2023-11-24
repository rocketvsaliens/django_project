from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from catalog.models import Product, Contact


def index(request):
    product_list = Product.objects.all().order_by('pk')
    paginator = Paginator(product_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        'title': 'Каталог товаров'
    }
    return render(request, 'catalog/index.html', context)


def show_item(request, product_pk):
    item = get_object_or_404(Product, pk=product_pk)
    context = {
        'item': item,
        'title': item
    }
    return render(request, 'catalog/item.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

    contact_list = [{
        'name': contact.name,
        'phone': contact.phone,
        'address': contact.address,
        'email': contact.email
    } for contact in Contact.objects.all()]

    context = {
        'title': 'Контакты',
        'contacts': contact_list
    }

    return render(request, "catalog/contacts.html", context)
