from rest_framework import serializers
from django.contrib.auth import get_user_model
from vendor.models import (
    Vendor,
    VendorDesign
)
from core.models import VendorUser

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['f_name', 'm_name', 'l_name', 'username', 'email', 'phone', 'role']

class VendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorUser
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'groups': {
                'read_only': True,
                'write_only': False,
                'required': False
            },
            'user_permissions': {
                'read_only': True,
                'write_only': False,
                'required': False
            },
            'vendor': {
                'read_only': True,
            },
            'last_login':{
                'read_only':True
            }
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        try:
            response['vendor'] = VendorSerializer(Vendor.objects.get(pk=response.get('vendor', None))).data
        except Exception as e:
            print(f"Error: {e}")
        return response

class VendorDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDesign
        fields = '__all__'
        read_only_fields = ['id', 'vendor', 'added_by', 'added_on']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['added_by'] is not None:
            response['added_by'] = UserSerializer(get_user_model().objects.get(pk=response['added_by'])).data
        return response
    
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['id']