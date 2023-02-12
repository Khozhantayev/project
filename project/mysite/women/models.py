from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class PostModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL ")
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name = 'time create')
    time_update = models.DateTimeField(auto_now=True, verbose_name = 'time update')
    is_published = models.BooleanField(default=True, verbose_name = 'is published')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name = 'category')
    # ('Category') в виде строки потому что первичный класс идет после вторичного, можно записать без скобок,
    # но в таком случае необходимо первичную модель вынести выше вторичной

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # класс для работы с моделью в админ панели:
    # название рубрики в единственном, множественном числе и порядок сортировки записей

    class Meta:
        verbose_name = "Blog post"
        verbose_name_plural = "Blog posts"
        ordering = ['title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='category')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Blog categories"
        ordering = ['id']


class ContactAdmin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    content = models.TextField(max_length=1000)

    def __str__(self):
        return self.email


    class Meta:
        verbose_name = "User feedback"
        verbose_name_plural = "User feedback"
        ordering = ['-id']
