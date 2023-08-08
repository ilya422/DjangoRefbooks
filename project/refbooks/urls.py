from django.urls import path
from .api import *

urlpatterns = [
    path('', refbooks_farm),
    path('<id>/elements', refbook_elements_farm)
]