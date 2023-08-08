from datetime import date
from http.client import NOT_FOUND, OK

from django.http import JsonResponse, HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
        # Заполнение фильтра
        _filter = {}
        if request.GET.get('date', None):
            versions = RefbookVersion.objects.filter(date__gte=request.GET['date']).all()
            _filter['id__in'] = [v.id for v in versions]

        # Получение записей
        refbooks = Refbook.objects.filter(**_filter).all()
        refbooks_serialized = RefbookAPISerializer(refbooks, many=True).data

        return JsonResponse(status=OK, data=refbooks_serialized, safe=False)


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
        # Заполнение фильтра
        _filter = {}
        if request.GET.get('version', None):
            version = RefbookVersion.objects.filter(refbook_id=id, version=request.GET['version']).last()
        else:
            version = RefbookVersion.objects.filter(refbook_id=id, date__lte=date.today()).latest('date')
        _filter['version'] = version.id if version else None

        # Получение записей
        refbook_elements = RefbookElement.objects.filter(**_filter).all()
        refbook_elements_serialized = RefbookElementAPISerializer(refbook_elements, many=True).data

        return JsonResponse(status=OK, data=refbook_elements_serialized, safe=False)


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
            version = RefbookVersion.objects.filter(refbook_id=id, version=request.GET['version']).last()
        else:
            version = RefbookVersion.objects.filter(refbook_id=id, date__lte=date.today()).latest('date')
        _filter['version'] = version.id if version else None

        # Получение записей
        refbook_elements = RefbookElement.objects.filter(**_filter).all()

        if refbook_elements:
            return HttpResponse(status=OK, content="Элемент найден")

        return HttpResponse(status=NOT_FOUND, content="Элемент не найден")
