from django.urls import path
from .api import *

urlpatterns = [
    path('', refbooks_farm),
]