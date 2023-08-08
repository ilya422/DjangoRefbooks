from collections import OrderedDict

from rest_framework import serializers

from .models import Refbook, RefbookElement


class RefbookAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook
        fields = ('id', 'code', 'name')


class RefbookElementAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = RefbookElement
        fields = ('code', 'value')
