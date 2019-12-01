from django.urls import path
from .views import *

urlpatterns = [
    path('addtest/', AddTestView.as_view()),
    path('removetest/', RemoveTestView.as_view()),
    path('gettests/', GetAllTestsView.as_view()),
    path('gettest/', GetTestView.as_view()),
    path('updatetest/', UpdateTestView.as_view()),
    path('removetest/', RemoveTestView.as_view()),
    path('nbofdone/', GetNbOfDoneView.as_view()),
    path('begintest/',BeginTestView.as_view()),
    path('continuetest/',ContinueTestView.as_view()),
    path('abletorun/',AbleToRun.as_view()),
    path('stoptest/',StopTest.as_view())
    
]