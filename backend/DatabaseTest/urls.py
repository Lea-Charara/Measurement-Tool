from django.urls import path
from .views import *

urlpatterns = [
    path('adddbtest/', AddDBTestView.as_view()),
    path('removedbtest/', RemoveDBTestView.as_view()),
    path('getdbtests/', GetAllDBTestsView.as_view())
]