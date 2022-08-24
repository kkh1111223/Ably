from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from django.contrib.auth import get_user_model
from django.contrib.auth import settings
from django.db.utils import IntegrityError

from ably_auth.biz import user_biz, session_biz
from ably_auth.serializers import user_serializer

User = get_user_model()
i18n = settings.I18N


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    queryset = User
    serializer_class = user_serializer.UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'reset_password'):
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        session = session_biz.validate_session(self.request.data.get('session_key'))
        if not session:
            return Response({"status": "failure"},
                            status=status.HTTP_403_FORBIDDEN)

        is_data_valid, msg = user_biz.check_create_request_data(request)
        if not is_data_valid:
            return Response({"status": "failure", "msg": msg},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.create_user(**request.data, is_staff=False, is_superuser=False)
        except IntegrityError:
            return Response({"status": "failure", "msg": i18n['resp_msg']['username_already_exist']},
                            status=status.HTTP_400_BAD_REQUEST)

        session.delete()
        return Response({"status": "success"},
                        status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True, url_path='my', url_name='my')
    def my_info(self, request, pk=None):
        has_perm = user_biz.compare_user_id(request.auth, pk)
        if not has_perm:
            return Response({"status": "failure"},
                            status=status.HTTP_403_FORBIDDEN)
        user_instance = self.get_object()
        serializer = self.get_serializer(user_instance)
        return Response({"status": "success", **serializer.data},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, authentication_classes=[],
            url_path='reset_password', url_name='reset_password')
    def reset_password(self, request, pk=None):
        # 핸드폰 번호에 해당 유저 유효성 검사
        session = session_biz.validate_session(self.request.data.get('session_key'))
        if not session:
            return Response({"status": "failure"},
                            status=status.HTTP_403_FORBIDDEN)

        u = User.objects.get(id=pk)
        u.set_password('123')
        u.save()
        session.delete()
        return Response({},
                        status=status.HTTP_200_OK)
