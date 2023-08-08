from django.urls import path
from .api import *

urlpatterns = [
    path('', refbooks_farm),
    path('<int:id>/elements', refbook_elements_farm),
    path('<int:id>/check_element', check_refbook_element)
]