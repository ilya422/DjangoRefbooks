from rest_framework import serializers

from .models import Refbook, RefbookElement


class RefbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook
        fields = '__all__'


class RefbookElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefbookElement
        fields = '__all__'
