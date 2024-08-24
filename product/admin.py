from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from product.models import Product, Category, Image, Attribute, AttributeValue, ProductAttribute


# Register your models here.

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Image)
# admin.site.register(Attribute)
# admin.site.register(AttributeValue)
# admin.site.register(ProductAttribute)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title', 'product_count')
    search_fields = ['title', 'id']
    prepopulated_fields = {'slug': ('title',)}

    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category_id', 'price', 'discount')
    search_fields = ['id', 'name', 'price']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category_id']

    # fields = ('price', 'discounted_price',)

    # def preview(self, obj):
    #     return mark_safe(f'<img src="{obj.image.url}" style="max-height: 20px;">')
    #
    # preview.short_description = 'Image'


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'product', 'is_primary')
    search_fields = ['id', 'product']
    list_filter = ['product']

    def is_primary(self, obj):
        return obj.is_primary()

    is_primary.boolean = True
    is_primary.short_description = 'Primary'

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 20px;">')

    preview.short_description = 'Image'


@admin.register(Attribute)
class AttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['id', 'name']
    list_filter = ['name']


@admin.register(AttributeValue)
class AttributeValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'value')
    search_fields = ['id', 'value']
    list_filter = ['value']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'attribute', 'value', 'product')
    search_fields = ['id', 'value', 'attribute', 'product']
    list_filter = ['product']
