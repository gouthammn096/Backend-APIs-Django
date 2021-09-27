from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from . import models


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    stream_name = serializers.ReadOnlyField(source='stream.stream_name')
    dept_name = serializers.ReadOnlyField(source='department.department_name')

    class Meta:
        model = models.User
        fields = ("id", "email", "first_name", "last_name", "password",
                  "confirm_password", "stream", "stream_name", "department", "dept_name", "mobile_number",
                  )

    def create(self, validated_data):
        del validated_data["confirm_password"]
        return super(UserRegistrationSerializer, self).create(validated_data)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return attrs


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(email=attrs.get("email"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")


class UserSerializer(serializers.ModelSerializer):

    stream_name = serializers.ReadOnlyField(source='stream.stream_name')
    dept_name = serializers.ReadOnlyField(source='department.department_name')

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'date_joined', 'email',
                  'mobile_number', 'stream', 'stream_name', 'department', 'dept_name'
                  )
        model = models.User
