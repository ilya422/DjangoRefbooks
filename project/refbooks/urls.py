from django.urls import path

from . import api


urlpatterns = [
    path('', api.RefbooksAPIView.as_view()),
    path('<int:id>/elements', api.RefbookElementsAPIView.as_view()),
    path('<int:id>/check_element', api.RefbookElementValidator.as_view())
]
