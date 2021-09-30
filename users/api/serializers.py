from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic = validated_data['patronymic'],
            phone = validated_data['phone'],
            type = validated_data['type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "patronymic", "type", "password" )