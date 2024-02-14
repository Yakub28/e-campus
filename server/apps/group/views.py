from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .logic.permissions import GroupPermissions
from .logic.serializers import GroupSerializer, JoinSerializer
from .models import Group


class GroupViewSet(viewsets.ModelViewSet):
    """ViewSet for Group model"""

    model = Group
    queryset = Group.objects.all()

    serializer_class = GroupSerializer

    permission_classes = [GroupPermissions]

    def get_queryset(self):
        """Return queryset for current user"""
        if self.request.user.is_authenticated:
            return self.queryset.filter(members__in=[self.request.user])
        return self.queryset.none()

    @swagger_auto_schema(methods=["get"], operation_id="Join group", query_serializer=JoinSerializer)
    @action(detail=False, methods=["get"])
    def join(self, request):
        """Join group with join_code"""
        serializer = JoinSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        group = Group.objects.filter(join_code=serializer.validated_data["join_code"]).first()

        if group:
            group.members.add(request.user)
            return Response({"detail": "Joined group"}, status=200)

        return Response({"detail": "Group not found"}, status=404)
