from django.urls import path
from .views import *

urlpatterns = [
    path('', CalendarView.as_view(), name='calendar_view'),
]