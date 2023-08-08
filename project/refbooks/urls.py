from django.urls import path

from . import api


urlpatterns = [
    path('', api.RefbooksAPIView.as_view(), name='refbooks'),
    path('<int:id>/elements', api.RefbookElementsAPIView.as_view(), name='refbook_elements'),
    path('<int:id>/check_element', api.RefbookElementValidator.as_view(), name='check_element')
]
