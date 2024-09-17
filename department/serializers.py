from rest_framework import serializers
from department.models import Department
from core.models import Staff

class StaffSerializer(serializers.ModelSerializer):
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
            },
            'last_login':{
                'read_only':True
            },
            'department':{
                'read_only':True
            }
        }

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['manager'] is not None:
            response['manager'] = StaffSerializer(Staff.objects.get(pk=instance.manager)).data
        return response
