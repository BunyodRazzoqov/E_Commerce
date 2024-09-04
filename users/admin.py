from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from users.models import User


# Register your models here.


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('email', 'username')


