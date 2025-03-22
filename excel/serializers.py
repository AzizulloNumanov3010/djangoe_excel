from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fullname", "work", "date_of_birth", "email", "phone_number", "created_at"]
