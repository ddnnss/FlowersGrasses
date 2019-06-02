from django.contrib import admin
from .models import *

class ImagesInline (admin.TabularInline):
    model = ItemImage
    readonly_fields = ('image_tag', )
    extra = 0


class ItemsInline (admin.TabularInline):
    model = Item
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag','name','article','price',]
    #list_display = [field.name for field in Item._meta.fields]
    inlines = [ImagesInline]
    search_fields = ('name_lower', 'article')
    list_filter = ('category', 'collection', 'is_active', 'is_present',)
    exclude = ['name_slug', 'buys', 'views', 'name_lower'] #не отображать на сранице редактирования
    class Meta:
        model = Item

class CategoryAdmin(admin.ModelAdmin):
    exclude = ['name_slug', 'views', ]
    class Meta:
        model = Category

class FilterAdmin(admin.ModelAdmin):
    exclude = ['name_slug', ]
    class Meta:
        model = Filter

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(ItemImage)
admin.site.register(Filter,FilterAdmin)
admin.site.register(Collection)
