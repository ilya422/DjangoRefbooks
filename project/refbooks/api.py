from django.http import JsonResponse

from .models import Refbook, RefbookVersion
from .serializers import RefbookSerializer


def refbooks_farm(request):
    """
    Функция для распределения методов запроса справочников
    """
    if request.method == 'GET':
        return get_refbooks(request)
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
