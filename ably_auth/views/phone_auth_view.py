from rest_framework import mixins, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ably_auth.models import phone_auth_model
from ably_auth.serializers import phone_auth_serializer
from ably_auth.utils import phone_auth_utils


class PhoneAuthViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.ListModelMixin):
    queryset = phone_auth_model.PhoneAuth
    serializer_class = phone_auth_serializer.PhoneAuthSerializer

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        is_data_valid, msg = phone_auth_utils.check_create_request_data(request)
        if not is_data_valid:
            return Response({"status": "FAIL", "msg": msg},
                            status=status.HTTP_400_BAD_REQUEST)

        code = phone_auth_utils.create_phone_auth(request, self.get_serializer())

        return Response({},
                        status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='validate', url_name='validate')
    def validate_code(self, request, pk=None, *args, **kwargs):
        return Response({"result": "yes"},
                        status=status.HTTP_200_OK)