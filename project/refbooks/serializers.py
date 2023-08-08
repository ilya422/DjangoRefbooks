from collections import OrderedDict

from rest_framework import serializers

from .models import Refbook, RefbookElement


class RefbookAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook
        fields = '__all__'

    def to_representation(self, instance):
        """
        Метод для очистки пустых полей
        """
        result = super().to_representation(instance)
        result = OrderedDict([(key, result[key]) for key in result if result[key]])
        return result


class RefbookElementAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = RefbookElement
        fields = ('code', 'value')
