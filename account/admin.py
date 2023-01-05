from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(MobileModel)
class MobileAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)


@admin.register(HallModel)
class HallAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)


@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)