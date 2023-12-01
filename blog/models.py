from django.db import models
from pytils.translit import slugify

NULLABLE = {
    'null': True, 'blank': True
}


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.CharField(max_length=200, unique=True, db_index=True, verbose_name='url')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog_images/', **NULLABLE, verbose_name='превью')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('title', 'created_on', 'is_published',)
