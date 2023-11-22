from django.shortcuts import render
from catalog.models import Product, Contact


def index(request):
    # Получаем 5 последних товаров, отсортированных по полю time_create в обратном порядке
    latest_products = Product.objects.order_by('-time_create')[:5]
    for one_product in latest_products:
        print(f'{one_product.description} {one_product.name} : {one_product.price} руб.')
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Главная страница'
    }
    return render(request, 'catalog/index.html', context)


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

    return render(request, "catalog/contacts.html", {'title': 'Контакты', 'contacts': contact_list})
