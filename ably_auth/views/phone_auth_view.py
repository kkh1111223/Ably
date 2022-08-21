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
        return Response({}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        is_data_valid, msg = phone_auth_utils.check_create_request_data(request)
        if not is_data_valid:
            return Response({"status": "fail", "msg": msg},
                            status=status.HTTP_400_BAD_REQUEST)

        serialized_data = phone_auth_utils.create_phone_authentication(request, self.get_serializer())
        return Response({"status": "success",
                         "verification_id": serialized_data['id'],
                         "verification_code": serialized_data['verification_code']},
                        status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='validate', url_name='validate')
    def verify_code(self, request, pk=None):
        instance = self.get_object()
        is_data_valid, msg = phone_auth_utils.check_verify_request_data(request)
        if not is_data_valid:
            return Response({"status": "fail", "msg": msg},
                            status=status.HTTP_400_BAD_REQUEST)

        verified, msg = phone_auth_utils.verify_phone_authentication(request, instance)
        if not verified:
            return Response({"status": "fail", "msg": msg},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "success"},
                        status=status.HTTP_200_OK)
