from dataclasses import fields
from rest_framework import serializers
from ..models import Reply
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Reply
        fields = ['id', 'content', 'user']