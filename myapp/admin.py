from django.contrib import admin
from .models import Package,Activity,PurchaseActivity
# Register your models here.


admin.site.register(Package)
admin.site.register(Activity)
admin.site.register(PurchaseActivity)