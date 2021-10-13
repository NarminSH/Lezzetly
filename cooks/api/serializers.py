from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from cooks.models import Cook, Recommendation, Resume

# valid_characters = 


class CookListSerializer(serializers.ModelSerializer):   #serializer for get method

    class Meta:
        model = Cook
        fields =(
            'id',
            'first_name',
            'last_name',
            'patronymic',
            'city',
            'work_experience',
            'rating',
            'is_available',
            'created_at',
            'updated_at',
        )
        read_only_fields = ['rating', ]


class CookSerializer(serializers.ModelSerializer): # serializer for put, patch and delete methods

    
    class Meta:
        model = Cook
        fields = (
            'id',
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'city',
            'service_place',  
            'payment_address',
            'birth_place',
            'city',
            'work_experience',
            'rating',
            'is_available',
            'created_at',
            'updated_at',
        )
        read_only_fields = ['rating', ]


        


class RecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommendation
        fields = (
            'id',
            'cook',
            'recommended_by',
            'created_at',
            'updated_at',
        )


class RecommendationListSerializer(RecommendationSerializer):
    cook = CookListSerializer()


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = (
            'id',
            'cook',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = ["cook", ]

        def save(self, attrs):
            request = self.context.get('request')
            print(request, 'requesttttttt')
            attrs['cook'] = request.user
            return super(ResumeSerializer, self).validate(attrs)


class ResumeListSerializer(ResumeSerializer):
    cook = CookListSerializer()