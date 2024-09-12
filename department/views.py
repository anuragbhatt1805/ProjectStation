from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from department.permissions import UpdateDeptPermission
from rest_framework.response import Response
from rest_framework.decorators import action
from department.serializers import (
    Department,
    StaffSerializer,
    DepartmentSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, UpdateDeptPermission, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]

    def get_serializer_class(self):
        if self.action == 'staffs':
            return StaffSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['get', 'post', 'delete'], url_path='staffs(?:/(?P<id>[^/.]+))?')
    def staffs(self, request, pk=None, id=None):
        department = self.get_object()
        if request.method == 'GET':
            if id:
                staff = department.get_staff(id)
                if staff:
                    return Response(StaffSerializer(staff).data)
                return Response({'message': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)
            staffs = department.list_staff()
            serializer = StaffSerializer(staffs, many=True)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            staff = department.remove_staff(id)
            if staff:
                return Response({'message': 'Staff deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'message': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = StaffSerializer(data=request.data)
            if serializer.is_valid():
                staff = department.add_staff(**serializer.data)
                return Response(StaffSerializer(staff).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)