from django.contrib import admin
from shop.models import *

# Register your models here.

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)

@admin.register(InvoiceModel)
class InvoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(InvoiceItemModel)
class InvoiceItemAdmin(admin.ModelAdmin):
    pass

@admin.register(OfflineInvoiceModel)
class OfflineInvoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(OfflineInvoiceItemModel)
class OfflineInvoiceItemAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    pass