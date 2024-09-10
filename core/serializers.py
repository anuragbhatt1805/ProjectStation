from django.utils.translation import gettext as _
from rest_framework import serializers
from core.models import (
    BaseUser,
    Client,
    Staff,
    VendorUser
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
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
            }
        }

    def create(self, validated_data):
        user = BaseUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class ClientSerializer(UserSerializer):
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


class StaffSerializer(UserSerializer):
    class Meta:
        model = Staff
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
            }
        }

    def create(self, validated_data):
        user = Staff.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class VendorUserSerializer(UserSerializer):
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
            }
        }

    def create(self, validated_data):
        user = VendorUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user