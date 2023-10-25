import re
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user

    def validate_password(self, value):
        pattern = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$'

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and contain at least one uppercase letter and one digit."
            )

        return value

    def validate(self, data):
        password = data.get('password')
        password1 = data.get('password2')

        if password and password1 and password != password1:
            raise serializers.ValidationError(
                "Passwords do not match."
            )

        return data
