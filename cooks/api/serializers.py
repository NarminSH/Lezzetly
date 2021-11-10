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

class CookCreateSerializer(serializers.ModelSerializer): # serializer for put, patch and delete methods

    
    class Meta:
        model = Cook
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'user_type',
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

class ShortCookCreateSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Cook
        fields = (
            'id',
            # 'username',
            # 'user_type',
            'first_name',
            'last_name',
            'email',
            'created_at',
            'updated_at',
        )


class CookSerializer(serializers.ModelSerializer): # serializer for put, patch and delete methods

    
    class Meta:
        model = Cook
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'user_type',
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



class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)



class RecommendationSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Recommendation
        fields = (
            'id',
            'cook',
            'recommended_by',
            'description',
            'created_at',
            'updated_at',
        )

        read_only_fields = ["cook", ]

        
        


class RecommendationListSerializer(RecommendationSerializer):
    cook = CookListSerializer()


class ResumeSerializer(DynamicFieldsModelSerializer):
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

        # def save(self, attrs):
        #     request = self.context.get('request')
        #     print(request, 'requesttttttt')
        #     attrs['cook'] = request.user
        #     return super(ResumeSerializer, self).validate(attrs)


class ResumeListSerializer(ResumeSerializer):
    cook = CookListSerializer()