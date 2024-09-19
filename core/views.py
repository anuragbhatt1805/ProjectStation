from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import viewsets, filters, status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from core.models import (
    BaseUser,
    Client,
    Staff,
    VendorUser
)
from core.serializers import (
    UserSerializer,
    ClientSerializer,
    StaffSerializer,
    VendorUserSerializer,
    ChangePasswordSerializer
)
from core.permissions import UpdateProfilePermission


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user Authentication Token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ChangePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = [TokenAuthentication, ]

    def put(self, request):
        # print(request.data)
        password = request.data['old_password']
        new_password = request.data['new_password']
        confirm_password = request.data['cnf_password']
        
        obj = get_user_model().objects.get(pk=request.user.id)
        if not obj.check_password(raw_password=password):
            print(request.data)
            print(obj)
            return Response({'non_field_errors': ['old password is incorrect']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            check = ChangePasswordSerializer(data=request.data)
            if check.is_valid():
                obj.set_password(new_password)
                obj.is_firstLogin = False
                obj.save()
                return Response({'success': 'password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(check.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientModelViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated, UpdateProfilePermission)
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['username', 'email', 'f_name', 'm_name', 'l_name', 'phone']

class StaffModelViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated, UpdateProfilePermission)
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['username', 'email', 'f_name', 'm_name', 'l_name', 'phone']

    def create(self, serializer):
        return super().create(serializer)

class VendorUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = VendorUserSerializer
    queryset = VendorUser.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated, UpdateProfilePermission)
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['username', 'email', 'f_name', 'm_name', 'l_name', 'phone']


class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = BaseUser.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        try:
            if self.request.user.is_superuser:
                return UserSerializer
            elif self.request.user.role == 'STAFF':
                return StaffSerializer
            elif self.request.user.role == 'CLIENT':
                return ClientSerializer
            elif self.request.user.role == 'VENDOR':
                return VendorUserSerializer
        except:
            return UserSerializer
    
    def get_queryset(self):
        try:
            if self.request.user.is_superuser:
                return BaseUser.objects.filter(pk=self.request.user.id)
            elif self.request.user.role == 'STAFF':
                return Staff.objects.filter(pk=self.request.user)
            elif self.request.user.role == 'CLIENT':
                return Client.objects.filter(pk=self.request.user.id)
            elif self.request.user.role == 'VENDOR':
                return VendorUser.objects.filter(pk=self.request.user.id)
        except Exception as e:
            return BaseUser.objects.filter(pk=self.request.user.id)
    
    def update(self, request, *args, **kwargs):
        if request.user.role == 'STAFF':
            serializer = StaffSerializer(data=request.data)
        elif request.user.role == 'CLIENT':
            serializer = ClientSerializer(data=request.data)
        elif request.user.role == 'VENDOR':
            serializer = VendorUserSerializer(data=request.data)
        else:
            serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        if request.user.role == 'STAFF':
            Staff.objects.get(id=kwargs['pk']).delete()
        elif request.user.role == 'CLIENT':
            Client.objects.get(id=kwargs['pk']).delete()
        elif request.user.role == 'VENDOR':
            VendorUser.objects.get(id=kwargs['pk']).delete()
        else:
            BaseUser.objects.get(id=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)