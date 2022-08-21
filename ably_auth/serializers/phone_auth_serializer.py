from rest_framework import serializers

from ably_auth.models import phone_auth_model


class PhoneAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = phone_auth_model.PhoneAuth
        fields = '__all__'
