from datetime import date

from django.http import JsonResponse, HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Refbook, RefbookVersion, RefbookElement
from .serializers import RefbookAPISerializer, RefbookElementAPISerializer


class RefbooksAPIView(APIView):
    """
    Методы справочников
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY, description="Дата начала действия в формате ГГГГ-ММ-ДД",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE)
        ]
    )
    def get(self, request):
        """
        Получение списка справочников
        :return: (JsonResponse) - список справочников
        """
        data = {
            "refbooks": []
        }

        # Заполнение фильтра
        _filter = {}
        if request.GET.get('date', None):
            versions = RefbookVersion.objects.filter(date__lte=request.GET['date']).all()
            if not versions:
                return JsonResponse(status=HTTP_204_NO_CONTENT, data=data, safe=False)
            _filter['id__in'] = [v.refbook.id for v in versions]

        # Получение записей
        refbooks = Refbook.objects.filter(**_filter).all()
        if not refbooks:
            return JsonResponse(status=HTTP_204_NO_CONTENT, data=data, safe=False)
        refbooks_serialized = RefbookAPISerializer(refbooks, many=True).data

        # Формирование ответа
        data["refbooks"] = refbooks_serialized
        return JsonResponse(status=HTTP_200_OK, data=data, safe=False)


class RefbookElementsAPIView(APIView):
    """
    Методы элементов справочников
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Идентификатор справочника",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('version', openapi.IN_QUERY, description="Версия справочника",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, id):
        """
        Получение списка элементов справочника
        :param id: (str) - Идентификатор справочника
        :return: (JsonResponse) - список элеметов справочника
        """
        data = {
            "elements": []
        }

        # Заполнение фильтра
        _filter = {}
        if request.GET.get('version', None):
            try:
                version = RefbookVersion.objects.filter(refbook_id=id, version=request.GET['version']).last()
            except RefbookVersion.DoesNotExist:
                return JsonResponse(status=HTTP_204_NO_CONTENT, data=data, safe=False)
        else:
            try:
                version = RefbookVersion.objects.filter(refbook_id=id, date__lte=date.today()).latest('date')
            except RefbookVersion.DoesNotExist:
                return JsonResponse(status=HTTP_204_NO_CONTENT, data=data, safe=False)
        _filter['version'] = version.id if version else None

        # Получение записей
        refbook_elements = RefbookElement.objects.filter(**_filter).all()
        if not refbook_elements:
            return JsonResponse(status=HTTP_204_NO_CONTENT, data=data, safe=False)
        refbook_elements_serialized = RefbookElementAPISerializer(refbook_elements, many=True).data


        # Формирование ответа
        data["elements"] = refbook_elements_serialized
        return JsonResponse(status=HTTP_200_OK, data=data, safe=False)


class RefbookElementValidator(APIView):
    """
    Методы валидации элементов списков
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Идентификатор справочника",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('code', openapi.IN_QUERY, description="Код элемента справочника",
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('value', openapi.IN_QUERY, description="Значение элемента справочника",
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('version', openapi.IN_QUERY, description="Версия справочника",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, id):
        """
        Валидация элемента справочника
        :param id: (str) - Идентификатор справочника
        :return: (HttpResponse) - Ответ на поиск элемента
        """
        # Заполнение фильтра
        _filter = {
            'code': request.GET['code'],
            'value': request.GET['value']
        }
        if request.GET.get('version', None):
            try:
                version = RefbookVersion.objects.filter(refbook_id=id, version=request.GET['version']).last()
            except RefbookVersion.DoesNotExist:
                return HttpResponse(status=HTTP_204_NO_CONTENT, content="Элемент не найден")
        else:
            try:
                version = RefbookVersion.objects.filter(refbook_id=id, date__lte=date.today()).latest('date')
            except RefbookVersion.DoesNotExist:
                return HttpResponse(status=HTTP_204_NO_CONTENT, content="Элемент не найден")
        _filter['version'] = version.id if version else None

        # Получение записей
        refbook_elements = RefbookElement.objects.filter(**_filter).all()
        if not refbook_elements:
            return HttpResponse(status=HTTP_204_NO_CONTENT, content="Элемент не найден")

        return HttpResponse(status=HTTP_200_OK, content="Элемент найден")
