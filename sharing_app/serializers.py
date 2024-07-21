from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import File
from django.core.mail import send_mail

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',)
        
class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
