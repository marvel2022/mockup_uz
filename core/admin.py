from django.contrib import admin

# Register your models here.

from .models import UseFullCategory, UseFull


class UseFullAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'link', 'free', 'paid', )
    list_display_links = ('name', )
    ordering = ('category', 'name', 'link', 'free', 'paid', )
    search_fields = ('category', 'name', 'link', 'free', 'paid', )
    list_editable = ('category', 'link', 'free', 'paid', )

    fieldsets = (
        ('Site Info', {
            "fields": (
                ('category', 'name', 'image', 'link', 'free', 'paid', )
            ),
        }),
    )

admin.site.register(UseFull, UseFullAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    list_display_links = ('name', )
    ordering = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    list_editable = ('slug',)

    prepopulated_fields = {'slug' : ('name',)}

    fieldsets = (
        ('Site Info', {
            "fields": (
                ('name', 'slug',)
            ),
        }),
    )

admin.site.register(UseFullCategory, CategoryAdmin)