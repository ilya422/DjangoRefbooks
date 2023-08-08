from django.urls import path

from . import views


urlpatterns = [
    path('', views.RefbooksAPIView.as_view()),
    path('<int:id>/elements', views.RefbookElementsAPIView.as_view()),
    path('<int:id>/check_element', views.RefbookElementValidator.as_view())
]
