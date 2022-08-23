from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from ably_auth.biz import user_biz
from ably_auth.serializers import user_serializer

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    queryset = User
    serializer_class = user_serializer.UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        # 필수항목 검사
        User.objects.create_user(**request.data)
        return Response({"status": "success"},
                        status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True, url_path='my', url_name='my')
    def my_info(self, request, pk=None):
        is_valid_access = user_biz.compare_user_id(self.request.auth, pk)
        if not is_valid_access:
            return Response({"status": "failure"},
                            status=status.HTTP_403_FORBIDDEN)
        user_instance = self.get_object()
        serializer = self.get_serializer(user_instance)
        return Response({"status": "success", **serializer.data},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='reset_password', url_name='reset_password')
    @permission_classes([])
    def reset_password(self, request, pk=None):
        return Response({},
                        status=status.HTTP_200_OK)