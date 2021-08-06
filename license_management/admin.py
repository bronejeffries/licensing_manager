from django.contrib import admin
from .models import License, Client
# Register your models here.


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('client', 'license_key',
                    'license_secret_key', 'created_on')
    list_filter = ('client__name', 'created_on')
    # fieldsets = (
    #     ('Advanced options', {
    #         'classes': ('collapse',),
    #         'readonly_fields': ('license_key', 'license_secret_key'),
    #     })
    # )


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'created_at')
    exclude = ('created_by',)
    list_filter = ('name', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


admin.site.register(License, LicenseAdmin)
admin.site.register(Client, ClientAdmin)
