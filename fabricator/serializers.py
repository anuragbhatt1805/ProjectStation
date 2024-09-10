from rest_framework import serializers
from fabricator.models import (
    Fabricator,
    StandardDesign
)
from core.models import Client

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

    def create(self, validated_data):
        user = Client.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class StandardDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardDesign
        fields = '__all__'
        read_only_fields = ['id', 'fabricator', 'added_by', 'added_on']
    
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['added_by'] = instance.added_by
    #     return response

class FabricatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricator
        fields = '__all__'
        read_only_fields = ['id']
    
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['designs'] = StandardDesignSerializer(instance.list_design(), many=True).data
    #     return response