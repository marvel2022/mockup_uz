from django.contrib import admin
from django.db.models import TextField
from tinymce.widgets import TinyMCE
from .models import (
    UserViews,
    Category,
    Product,
    MockUp,
    Image,
    Tag,
)
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    #  ('name', 'slug', 'image', 'caption', )
    list_display  = ('name', 'slug', 'active',)
    orderinig     = ('name', 'slug', 'active', )
    list_display_links = ('name',)
    list_editable = ('slug', 'active',)
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Category', {
            "fields": (
                'name', 'slug', 'active', 'image', 'caption'
            ),
        }),
    )

admin.site.register(Category, CategoryAdmin)


class ImageAdminTabularInline(admin.TabularInline):
    model   = Image
    min_num = 1

# class MockUpTabularInline(admin.TabularInline):
#     model   = MockUp
#     min_num = 1

class ProductAdmin(admin.ModelAdmin):
    # ('category', 'name', 'slug', 'description', 'price', 'discount', 'paid', 'free', 'downloaded', 'viewed', 'liked', 'tags', )

    inlines = [ImageAdminTabularInline,]

    list_display = ('category', 'name', 'price', 'discount', 'paid', 'free', 'resolution', 'extension', 'downloaded', )
    list_display_links = ('name', 'downloaded',)
    ordering = ('category', 'name', 'price', 'discount', 'paid', 'free', 'downloaded', 'tags')
    search_fields = ('category', 'name', 'price', 'discount', 'paid', 'free', 'downloaded', 'tags')

    list_editable = ('category', 'price', 'discount', 'paid', 'free', 'resolution', 'extension', )

    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Category', {
            "fields": (
                'category',
            ),
        }),
        ('MockUp Info', {
            "fields": (
                'name', 'slug', 'description', 'tags', 'file', 'resolution', 'extension',
            )
        }),
        ('Price Info', {
            'fields' : (
                'price', 'discount', 'paid', 'free',
            )
        }),
        # ('Likes', {
        #     'fields' : (
        #         'liked',
        #     )
        # }),
    )

    formfield_overrides = {
        TextField: {'widget': TinyMCE }
    }    


admin.site.register(Product, ProductAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    list_display_links = ('tag',)
    ordering = ('tag',)
    search_fields = ('tag',)
    # list_editable = ('category',)

    fieldsets = (
        ('Tags', {
            "fields": (
                'tag',
            ),
        }),
    )

admin.site.register(Tag, TagAdmin)

admin.site.register(UserViews)

