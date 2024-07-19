from rest_framework.fields import empty

from .models import *
from rest_framework import serializers
from django.conf import settings


class PublicSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PublicChat
        fields = ['chat_name', 'description', 'owner', 'host_name', 'slug']


