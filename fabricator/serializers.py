from rest_framework import serializers
from fabricator.models import (
    Fabricator,
    StandardDesign
)
from core.models import Client
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['f_name', 'm_name', 'l_name', 'username', 'email', 'phone', 'role']

class FabricatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricator
        fields = '__all__'
        read_only_fields = ['id']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
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
            'fabricator': {
                'read_only': True,
            },
            'last_login':{
                'read_only':True
            }
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        try:
            response['fabricator'] = FabricatorSerializer(Fabricator.objects.get(pk=response.get('fabricator', None))).data
        except Exception as e:
            print(f"Error: {e}")
        return response

class StandardDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardDesign
        fields = '__all__'
        read_only_fields = ['id', 'fabricator', 'added_by', 'added_on']
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['added_by'] is not None:
            response['added_by'] = UserSerializer(get_user_model().objects.get(pk=response['added_by'])).data
        return response