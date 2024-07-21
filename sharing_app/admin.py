from django.contrib import admin
from sharing_app.models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','is_active','user_type','password']

class FileAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(File, FileAdmin)