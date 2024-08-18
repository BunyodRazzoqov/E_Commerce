from django.contrib import admin
from django.utils.safestring import mark_safe

from product.models import Product, Category, Image, Attribute, AttributeValue, ProductAttribute

# Register your models here.

# admin.site.register(Product)
# admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'product_count')
    search_fields = ['title', 'id']
    prepopulated_fields = {'slug': ('title',)}

    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category_id', 'price', 'discount', 'preview')
    search_fields = ['id', 'name', 'price']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category_id']

    # fields = ('price', 'discounted_price',)

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 20px;">')

    preview.short_description = 'Image'
