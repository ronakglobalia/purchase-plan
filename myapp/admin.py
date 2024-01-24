from django.contrib import admin
from .models import Package, Activity, PurchaseActivity
# Register your models here.


class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'price', 'total_activity')


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'activity_task')


class PurchaseActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'total_activity', 'grandtotal')


admin.site.register(Package, PackageAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(PurchaseActivity, PurchaseActivityAdmin)