from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from vendor.models import (
    Vendor,
)
from vendor.serializers import (
    VendorSerializer,
    VendorDesignSerializer,
    VendorUserSerializer
)
from vendor.permissions import UpdateVendorPermission

class VendorModelViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, UpdateVendorPermission, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'state', 'country', 'zip_code']

    def get_serializer_class(self):
        if self.action == 'designs':
            return VendorDesignSerializer
        elif self.action == 'users':
            return VendorUserSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['get', 'post', 'delete'], url_path='designs(?:/(?P<id>[^/.]+))?')
    def designs(self, request, pk=None, id=None):
        vendor = self.get_object()
        if request.method == 'GET':
            if id:
                design = vendor.get_design(id)
                if design:
                    return Response(VendorDesignSerializer(design).data)
                return Response({'message': 'Design not found.'}, status=status.HTTP_404_NOT_FOUND)
            designs = vendor.list_design()
            serializer = VendorDesignSerializer(designs, many=True)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            design = vendor.remove_design(id)
            if design:
                return Response({'message': 'Design deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'message': 'Design not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = VendorDesignSerializer(data=request.data)
            if serializer.is_valid():
                design = vendor.add_design(file=request.data.get('file'), added_by=request.user)
                return Response(VendorDesignSerializer(design).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get', 'post', 'delete'], url_path='users(?:/(?P<id>[^/.]+))?')
    def users(self, request, pk=None, id=None):
        vendor = self.get_object()
        if request.method == 'GET':
            if id:
                user = vendor.get_user(id)
                if user:
                    return Response(VendorUserSerializer(user).data)
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            users = vendor.list_user()
            serializer = VendorUserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            user = vendor.remove_user(id)
            if user:
                return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = VendorUserSerializer(data=request.data)
            if serializer.is_valid():
                user = vendor.add_user(**serializer.data)
                return Response(VendorUserSerializer(user).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)