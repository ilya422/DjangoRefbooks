from datetime import date
from django.http import JsonResponse

from .models import Refbook, RefbookVersion, RefbookElement
from .serializers import RefbookSerializer, RefbookElementSerializer


def refbooks_farm(request):
    """
    Функция для распределения методов запроса справочников
    """
    if request.method == 'GET':
        return get_refbooks(request)
    else:
        return JsonResponse(status=400, data={}, safe=False)


def refbook_elements_farm(request, **kwargs):
    """
    Функция для распределения методов запроса элементов справочника
    """
    if request.method == 'GET':
        return get_refbook_elements(request, kwargs['id'])
    else:
        return JsonResponse(status=400, data={}, safe=False)


def get_refbooks(request):
    """
    Функция для получения списка справочников
    :param request: Объект запроса
    :return: JSON
    """
    # Заполнение фильтра
    _filter = {}
    if request.GET.get('date', None):
        versions = RefbookVersion.objects.filter(date__gte=request.GET['date']).all()
        _filter['id__in'] = [v.id for v in versions]

    # Получение записей
    refbooks = Refbook.objects.filter(**_filter).all()
    refbooks_serialized = RefbookSerializer(refbooks, many=True).data

    # Очистка пустых полей
    for serialized in refbooks_serialized:
        for k, v in serialized.items():
            if not v:
                del serialized[k]

    return JsonResponse(status=200, data=refbooks_serialized, safe=False)


def get_refbook_elements(request, refbook_id):
    """
    Функция для получения списка элементов справочника
    :param request: Объект запроса
    :param refbook_id: ID справочника
    :return: JSON
    """
    version = None

    # Заполнение фильтра
    _filter = {}
    if request.GET.get('version', None):
        version = RefbookVersion.objects.filter(refbook_id=refbook_id, version=request.GET['version']).latest()
    else:
        version = RefbookVersion.objects.filter(refbook_id=refbook_id, date__lte=date.today()).latest('date')
    _filter['version'] = version.id

    # Получение записей
    refbook_elements = RefbookElement.objects.filter(**_filter).all()
    refbook_elements_serialized = RefbookElementSerializer(refbook_elements, many=True).data

    return JsonResponse(status=200, data=refbook_elements_serialized, safe=False)
