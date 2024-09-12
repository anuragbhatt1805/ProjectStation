from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from fabricator.models import (
    Fabricator,
)
from fabricator.serializers import (
    FabricatorSerializer,
    StandardDesignSerializer,
    ClientSerializer
)
from fabricator.permissions import UpdateFabPermission

class FabricatorModelViewSet(viewsets.ModelViewSet):
    serializer_class = FabricatorSerializer
    queryset = Fabricator.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated, UpdateFabPermission)
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', 'address', 'city', 'state', 'country', 'zip_code', 'website', 'drive']

    def get_serializer_class(self):
        if self.action == 'designs':
            return StandardDesignSerializer
        elif self.action == 'clients':
            return ClientSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['get', 'post', 'delete'], url_path='designs/(?P<id>[^/.]+)')
    def designs(self, request, pk=None, id=None):
        fabricator = self.get_object()
        if request.method == 'GET':
            if id:
                design = fabricator.get_design(id)
                if design:
                    return Response(StandardDesignSerializer(design).data)
                return Response({'message': 'Design not found.'}, status=status.HTTP_404_NOT_FOUND)
            designs = fabricator.list_design()
            serializer = StandardDesignSerializer(designs, many=True)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            design = fabricator.remove_design(id)
            if design:
                return Response({'message': 'Design deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'message': 'Design not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = StandardDesignSerializer(data=request.data)
            if serializer.is_valid():
                design = fabricator.add_design(file=request.data.get('file'), added_by=request.user)
                return Response(StandardDesignSerializer(design).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post', 'delete'], url_path='clients/(?P<id>[^/.]+)')
    def clients(self, request, pk=None, id=None):
        fabricator = self.get_object()
        if request.method == 'GET':
            if id:
                client = fabricator.get_contact(id)
                if client:
                    return Response(ClientSerializer(client).data)
                return Response({'message': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)
            clients = fabricator.list_contact()
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            client = fabricator.remove_contact(id)
            if client:
                return Response({'message': 'Client removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'message': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                client = fabricator.add_contact(**serializer.data)
                return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)