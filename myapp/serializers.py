from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Activity,PurchaseActivity

# from .models import package


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ['username','first_name','last_name','password']

    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)

class ActivitySerializer(serializers.ModelSerializer):
    # package = serializers.SerializerMethodField()

    class Meta:
      model = Activity
      fields = ['user','package','activity_task']

    # def get_package(self, obj):
    #     print('-------obj---',obj)
    #     name = obj.package__package_name
    #     print('name-------------------',name)
    #     return name

class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
      model = PurchaseActivity
      fields = ['user','package','total_activity','grandtotal']
