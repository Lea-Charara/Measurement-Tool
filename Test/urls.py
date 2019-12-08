from django.urls import path
from .views import *

urlpatterns = [
    path('addtest/', AddTestView.as_view()),
    path('removetest/', RemoveTestView.as_view()),
    path('gettests/', GetAllTestsView.as_view()),
    path('gettest/', GetTestView.as_view()),
    path('updatetest/', UpdateTestView.as_view()),
    path('removetest/', RemoveTestView.as_view()),
    path('progress/', GetProgressView.as_view()),
    path('begintest/',BeginTestView.as_view()),
    path('abletorun/',Status.as_view()),
    path('stoptest/',StopTest.as_view()),
    path('restart/',RestartTestView.as_view())
    
]