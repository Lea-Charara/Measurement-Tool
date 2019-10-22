from django.urls import path
from .views import *

urlpatterns = [
    path('getypename/', GetTypeName.as_view())
    ]