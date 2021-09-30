from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from users.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            patronymic = validated_data['patronymic'],
            phone = validated_data['phone'],
            user_type = validated_data['user_type'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("first_name", 
                    "last_name", 
                    "phone", 
                    "patronymic", 
                    "user_type", 
                    "password" )



class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label=("Password",),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'password'
        )

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        if phone and password:
            user = authenticate(request=self.context.get('request'),
                                phone=phone, password=password)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "phone" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return super(UserDetailSerializer, self).validate(attrs)