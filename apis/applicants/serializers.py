from .models import Applicant, AchievementDocument
from rest_framework import serializers
from django.contrib.auth.models import Permission



class AchievementDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementDocument
        fields = ['id', 'name', 'document', 'description']


class ApplicantSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    nationality = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    primary_location = serializers.CharField(max_length=100, required=True)
    past_achievement_documents = AchievementDocumentSerializer(many=True, required=False)

    class Meta:
        model = Applicant
        fields = ['id', 'applicant_id', 'first_name', 'last_name', 'nationality', 'gender', 'email',
                   'primary_location', 'secondary_location', 'guardian1_name', 'guardian1_contact',
                   'date_of_birth', 'phone', 'id_card_number', 'scanned_id_document', 'profile_picture',
                   'guardian2_name', 'guardian2_contact', 'motivation_letter', 'past_achievement_documents']
        read_only_fields = ['applicant_id', 'past_achievement_documents']



