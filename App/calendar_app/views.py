from django.shortcuts import render, redirect
from django.db.models.query import QuerySet, Q
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.views.generic import ListView
from .models import CalendarDay
from .utils import Calendar
import calendar
from django.utils.safestring import mark_safe
from django.contrib import messages


class CalendarView(ListView):
    model = CalendarDay
    template_name = 'calendar_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month',None))
        cal = Calendar(d.year, d.month)
        start_date = datetime(d.year, d.month, 1)
        end_date = datetime(d.year, d.month, 28)
        events = CalendarDay.objects.filter(Q(datetime__range=(start_date, end_date)))
        events_exists = len(events) > 2
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['events_exists'] = events_exists
        return context
    
    def post(self, request, *args, **kwargs):
        month = int(self.request.POST.get("month"))
        year = int(self.request.POST.get("year"))
        days = self.request.POST.getlist("days")
        teams = self.request.POST.getlist("teams")
        if "save_changes" in self.request.POST:
            for i in range(len(days)):
                day = int(days[i])
                team = teams[i]
                date = datetime(year,month,day)
                instance = CalendarDay.objects.create(datetime=date, team=team)
                instance.save()
            messages.success(request, "New Calendar Saved successfully!")
        elif "reset_calendar" in self.request.POST:
            for i in range(len(days)):
                day = int(days[i])
                team = teams[i]
                date = datetime(year,month,day)
                instance = CalendarDay.objects.filter(datetime=date, team=team).delete()
            messages.success(request, f"Calendar Month: {month} Reset successfully!")                
        return redirect("calendar_view")

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
