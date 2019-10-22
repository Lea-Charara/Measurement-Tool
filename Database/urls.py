from django.urls import path
from .views import *

urlpatterns = [
    path('adddatabase/', AddDatabaseView.as_view()),
    path('removedatabase/', RemoveDatabaseView.as_view()),
    path('getdatabases/', GetAllDataBasesView.as_view())
    ]