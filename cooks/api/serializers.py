from rest_framework import serializers
from cooks.models import Cook, Recommendation, Resume

# evez edir Category Listi ni
class CookListSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Cook
        fields =(
            'id',
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'birth_place',
            'city',
            'service_place',
            'payment_address',
            'work_experience',
            'rating',
            'is_available',
            'created_at',
            'updated_at',
            'recommendations',
            'resumes',
        )
        
# evez edir Meal i
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


class ResumeListSerializer(ResumeSerializer):
    cook = CookListSerializer()