from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Package(models.Model):
    package_name = models.CharField(max_length=19)
    price = models.IntegerField(default=0)
    total_activity = models.IntegerField(default=0)

    def __str__(self):
        return self.package_name
        
    
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE,null=True,blank=True)
    activity_task = models.CharField(max_length=19 ,null =True,blank = True)


class PurchaseActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    total_activity = models.IntegerField(default=0, null=True, blank=True)
    grandtotal = models.IntegerField(default=0, null=True, blank=True)
