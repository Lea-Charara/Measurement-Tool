from django.urls import path
from .views import *

urlpatterns = [
    path('adddbtest/', AddDBTestView.as_view()),
    path('removedbtest/', RemoveDBTestView.as_view()),
    path('getalldbtests/', GetAllDBTestsView.as_view()),
    path('getdbtests/', GetDBTestView.as_view()),
    path('removedbtestid/', RemoveDBTestView_byTest_id.as_view()),
    path('Times/',GetTimes.as_view()),
    path('GetProgress/',GetProgress.as_view())
]