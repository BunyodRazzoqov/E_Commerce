from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

from my_web.models import Customer

# Register your models here.


# admin.site.register(Customer)
# admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display: tuple = ('full_name', 'email', 'phone', 'address')  # preview_image
    search_fields: list = ['full_name', 'email', 'address']
    list_filter: list = ['address']
    prepopulated_fields: dict = {'slug': ('full_name',)}

    """
    image uchun
    def preview_image(self, obj):
        if obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')

    preview_image.short_description = 'Image'
    """
