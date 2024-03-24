from django.urls import path
from .views import *

urlpatterns = [
    path('employees_list/', EmployeeList.as_view(), name='employees'),
    path('search_employee/', SearchEmployee.as_view(), name="search_employee"),
    path('new_employees/', CreateEmployees.as_view(), name="create_employees"),
    path('update_employee/<int:pk>/', UpdateEmployee.as_view(), name='update_employee'),
    path('delete_employee/<int:pk>/', DeleteEmployee.as_view(), name='delete_employee'),

    path('guests_list/', GuestList.as_view(), name='guests'),
    path('new_guest/', CreateGuest.as_view(), name='create_guest'),    
    path('update_guest/<int:pk>/', UpdateGuest.as_view(), name='update_guest'),
    path('delete_guest/<int:pk>/', DeleteGuest.as_view(), name='delete_guest'),

    path('leaves_list/', LeaveList.as_view(), name='leaves'),
    path('all_leaves_list/', AllLeaveList.as_view(), name='all_leaves'),
    path('new_leave/', CreateLeave.as_view(), name='create_leave'),
    path('update_leave/<int:pk>/', UpdateLeave.as_view(), name='update_leave'),
    path('delete_leave/<int:pk>/', DeleteLeave.as_view(), name='delete_leave'),
]