from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, View
from .models import *
from . forms import *
from django.urls import reverse_lazy
from django.db.models.query_utils import Q
from datetime import datetime, timedelta


class EmployeeList(ListView):
    context_object_name = "employees"
    queryset = Employee.objects.all()
    template_name = "user/employees_list.html"
    paginate_by = 100
    ordering = ["name"]


class SearchEmployee(ListView):
    model = Employee
    template_name = "user/employees_list.html"
    context_object_name = "employees"
    paginate_by = 100
    
    def get_queryset(self):
        query = self.request.GET.get('searchEmployee')
        object_list = Employee.objects.filter(
            Q(name__icontains=query) | Q(card_number1__icontains=query) |
            Q(card_number2__icontains=query) | Q(card_number3__icontains=query)| Q(ace__icontains=query)) 
        return object_list
    

class CreateEmployees(View):
    def get(self, request):
        employee_formset = EmployeeCreationFormSet(request.GET or None)
        context = {
            'employee_formset': employee_formset,
        }
        return render(request, 'user/new_employee.html', context)
    
    def post(self, request):
        employee_formset = EmployeeCreationFormSet(request.POST)
        context = {
            'employee_formset': employee_formset,
        }
        if request.method == 'POST' and 'save_users' in request.POST:
            employee_formset = EmployeeCreationFormSet(request.POST)
            if employee_formset.is_valid():
                for form in employee_formset:
                    if form.instance.name != '':
                        if form.is_valid():
                            instance = form.save(commit=False)
                            instance.save()
                        else:
                            messages.error(request, "Error at creating the employee: " + str(form.errors))
                            return redirect('create_employees')
                    else:
                        messages.error(request, "Error at creating the employee: Field NAME can not be empty")
                        return redirect('create_employees')
                messages.success(request, "Employee(s) registered correctly")
                return redirect('employees')
            else:
                messages.error(request, "Error at creating the employee: " + str(employee_formset.errors))
                return redirect('create_employees')                    
        return render(request, 'user/new_employee.html', context)


class UpdateEmployee(UpdateView):
    model = Employee
    form_class = EmployeeCreationForm
    template_name = 'user/update_employee.html'
    success_url = reverse_lazy('employees')


class DeleteEmployee(DeleteView):
    model = Employee
    success_url = reverse_lazy('employees')
    success_message = "Employee successfully deleted from Data Base"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteEmployee, self).delete(request, *args, **kwargs)
    

class GuestList(ListView):
    context_object_name = "guests"
    start_time = datetime(datetime.now().year,datetime.now().month,1)
    month_ahead = datetime(datetime.now().year,datetime.now().month +1,1)
    end_time = month_ahead - timedelta(days=1)
    # queryset = Guest.objects.filter(Q(start_date__range=(start_time, end_time)) | Q(end_date__gte=datetime.now()))
    queryset = Guest.objects.all()
    template_name = "user/guests_list.html"
    paginate_by = 100
    ordering = ["start_date"]


class CreateGuest(View):
    def get(self, request):
        guest_form = GuestCreationForm(request.GET or None)
        context = {
            'guest_form': guest_form,
        }
        return render(request, 'user/new_guest.html', context)
    
    def post(self, request):
        guest_form = GuestCreationForm(request.POST)
        context = {
            'guest_form': guest_form,
        }
        if guest_form.is_valid():
            guest_form.save()
            messages.success(request, "Guest Card registered correctly")
            return redirect('guests')
        else:
            messages.error(request, "Error at creating the Guest card:" + str(guest_form.errors))
            return redirect('create_guest', context)        
        

class UpdateGuest(UpdateView):
    model = Guest
    form_class = GuestCreationForm
    template_name = 'user/update_guest.html'
    success_url = reverse_lazy('guests')


class DeleteGuest(DeleteView):
    model = Guest
    success_url = reverse_lazy('guests')
    success_message = "Guest Card successfully deleted from Data Base"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteGuest, self).delete(request, *args, **kwargs)
    

class LeaveList(ListView):
    context_object_name = "leaves"
    start_time = datetime(datetime.now().year,datetime.now().month,1)
    month_ahead = datetime(datetime.now().year,datetime.now().month +1,1)
    end_time = month_ahead - timedelta(days=1)
    # queryset = Leave.objects.filter(Q(start_date__range=(start_time, end_time)) | Q(end_date__gte=datetime.now()))
    queryset = Leave.objects.all()
    template_name = "user/leaves_list.html"
    paginate_by = 100
    ordering = ["start_date"]


class AllLeaveList(ListView):
    context_object_name = "leaves"    
    queryset = Leave.objects.all()
    template_name = "user/all_leaves_list.html"
    paginate_by = 100
    ordering = ["start_date"]


class CreateLeave(View):
    def get(self, request):
        leave_form = LeaveCreationForm(request.GET or None)
        context = {
            'leave_form': leave_form,
        }
        return render(request, 'user/new_leave.html', context)
    
    def post(self, request):
        leave_form = LeaveCreationForm(request.POST)
        context = {
            'leave_form': leave_form,
        }
        if leave_form.is_valid():
            leave_form.save()
            messages.success(request, "Leave registered correctly")
            return redirect('leaves')
        else:
            messages.error(request, "Error at creating the Leaves:" + str(leave_form.errors))
            return redirect('create_leave', context)        
        

class UpdateLeave(UpdateView):
    model = Leave
    form_class = LeaveCreationForm
    template_name = 'user/update_leave.html'
    success_url = reverse_lazy('leaves')


class DeleteLeave(DeleteView):
    model = Leave
    success_url = reverse_lazy('leaves')
    success_message = "Leaves successfully deleted from Data Base"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteLeave, self).delete(request, *args, **kwargs)