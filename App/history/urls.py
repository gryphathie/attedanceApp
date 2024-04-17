from django.urls import path
from .views import *

urlpatterns = [
    path('import/', CsvHistoryView.as_view(), name='import_history'),
    path('history/', SearchEmployeeAttendance.as_view(), name='history'),
    path('attendance_table/', AttendanceTable.as_view(), name='attendance_table'),
]