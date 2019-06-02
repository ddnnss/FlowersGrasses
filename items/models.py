from django.db import models
from pytils.translit import slugify
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.utils.safestring import mark_safe


import os


def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num

class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение категории', upload_to='category_img/', blank=False)
    page_title = models.CharField('Название страницы', max_length=255, blank=False, null=True)
    page_description = models.CharField('Описание страницы', max_length=255, blank=False, null=True)
    page_keywords = models.TextField('Keywords', blank=False, null=True)
    short_description = models.TextField('Краткое описание для главной', blank=True,)
    description = RichTextUploadingField('Описание категории', blank=True, null=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return 'id :%s , %s ' % (self.id, self.name)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"



class Filter(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True,on_delete=models.SET_NULL, verbose_name='Категория')
    name = models.CharField('Название фильтра', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Filter, self).save(*args, **kwargs)

    def __str__(self):
        return '%s | %s ' % (self.category.name, self.name)

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"


class Collection(models.Model):
    name = models.CharField('Название коллекции', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение коллекции', upload_to='collection_img/', blank=False)
    page_title = models.CharField('Название страницы', max_length=255, blank=False, null=True)
    page_description = models.TextField('Описание страницы', blank=False, null=True)
    page_keywords = models.TextField('Keywords', blank=False, null=True)
    description = RichTextUploadingField('Описание коллекции', blank=True, null=True)

    views = models.IntegerField(default=0)
    show_at_homepage = models.BooleanField('Отображать на главной', default=True)
    show_at_category = models.BooleanField('Отображать в категории', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"


class Item(models.Model):
    collection = models.ForeignKey(Collection, blank=True, null=True, on_delete=models.SET_NULL,db_index=True, verbose_name='В коллекции')
    filter = models.ForeignKey(Filter, blank=True, null=True, on_delete=models.SET_NULL,db_index=True, verbose_name='Фильтр')
    category = models.ForeignKey(Category, blank=False, null=True, verbose_name='Подкатегория', on_delete=models.SET_NULL,db_index=True)
    name = models.CharField('Название товара', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True,default='')
    name_slug = models.CharField(max_length=255, blank=True, null=True,db_index=True)
    price = models.IntegerField('Цена', blank=False, default=0, db_index=True)
    page_title = models.CharField('Название страницы', max_length=255, blank=False, null=True)
    page_description = models.TextField('Описание страницы',  blank=False, null=True)
    description = RichTextUploadingField('Описание товара', blank=True, null=True)
    article = models.CharField('Артикул', max_length=50, blank=False, null=True)
    color = models.CharField('Цвет',  max_length=15, blank=True, null=True)
    is_active = models.BooleanField('Отображать товар ?', default=True, db_index=True)
    is_present = models.BooleanField('Товар в наличии ?', default=True, db_index=True)
    buys = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        self.name_lower = self.name.lower()
        super(Item, self).save(*args, **kwargs)

    def getfirstimage(self):
        url = None
        for img in self.itemimage_set.all():
            if img.is_main:
                url = img.image_small.url
        return url

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.getfirstimage():
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.getfirstimage()))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Основная картинка'

    def __str__(self):
        if self.filter:
            return 'id:%s %s | Фильтр %s' % (self.id, self.name, self.filter.name)
        else:
            return 'id:%s %s | Фильтра нет' % (self.id, self.name)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"



class ItemImage(models.Model):
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField('Изображение товара', upload_to='item_images', blank=False)
    image_small = ImageSpecField(source='image',processors=[ResizeToFill(300, 300)], format='JPEG', options={'quality':80})
    is_main = models.BooleanField('Основная картинка ?', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s Изображение для товара : %s ' % (self.id, self.item.name)

    class Meta:
        verbose_name = "Изображение для товара"
        verbose_name_plural = "Изображения для товара"

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.image_small:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image_small.url))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Картинка'





