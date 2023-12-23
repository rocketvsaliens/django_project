from django.db import models

NULLABLE = {
    'null': True, 'blank': True
}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(max_length=1000, **NULLABLE, verbose_name='описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='наименование')
    description = models.TextField(max_length=2200, **NULLABLE, verbose_name='описание')
    photo = models.ImageField(upload_to='photos/', verbose_name='изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена', default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['pk']


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.CharField(max_length=8, verbose_name='Номер версии')
    title = models.CharField(max_length=30, **NULLABLE, verbose_name='Название версии')
    is_actual = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Версию'
        verbose_name_plural = 'Версии'
        ordering = ['number']


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    address = models.CharField(max_length=255, verbose_name='адрес')
    phone = models.CharField(max_length=100, verbose_name='телефон')
    email = models.EmailField(verbose_name='email')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        ordering = ['pk']
