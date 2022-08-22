from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from ably_auth.serializers import user_serializer

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = User
    serializer_class = user_serializer.UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        return Response({},
                        status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        return Response({},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='reset_password', url_name='reset_password')
    @permission_classes([])
    def reset_password(self, request, pk=None):
        return Response({},
                        status=status.HTTP_200_OK)