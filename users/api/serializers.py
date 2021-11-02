from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from users.models import User
from cooks.models import Cook
from delivery.models import Courier

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    user_type = serializers.CharField(required=True)

    def create(self, validated_data):
        user_type = validated_data['user_type']
        if user_type == '1':  #checking user's type beforehand to know in which model to save instance
            CurrentModel = Cook
        elif user_type == '2':
            CurrentModel = Courier
        else:
            CurrentModel = User
            
        user = CurrentModel.objects.create(
        first_name = validated_data['first_name'],
        last_name = validated_data['last_name'],
        patronymic = validated_data['patronymic'],
        phone = validated_data['phone'],
        user_type = validated_data['user_type'],
        email = validated_data['email']
    )
    
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = (  
                    "id",
                    "first_name", 
                    "last_name", 
                    "phone", 
                    "patronymic", 
                    "user_type", 
                    "password",
                    'email' 
                    )



class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = Cook
        # fields = ('token','password',)
        # read_only_fields = ['token']


# class UserDetailSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         label=("Password",),
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True
#     )

#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'first_name',
#             'last_name',
#             'patronymic',
#             'phone',
#             'password',
#             'email'
#         )

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         if email and password:
#             user = authenticate(request=self.context.get('request'),
#                                 email=email, password=password)
#             if not user:
#                 msg = ('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = ('Must include "email" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')

#         attrs['user'] = user
#         return super(UserDetailSerializer, self).validate(attrs)