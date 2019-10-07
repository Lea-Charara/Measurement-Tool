from django.urls import path
from .views import *

urlpatterns = [
    path('addtest/', AddTestView.as_view()),
    path('removetest/', RemoveTestView.as_view()),
    path('gettests/', GetAllTestsView.as_view())
]