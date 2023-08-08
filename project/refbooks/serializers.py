from rest_framework import serializers

from .models import Refbook


class RefbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook
        fields = '__all__'
