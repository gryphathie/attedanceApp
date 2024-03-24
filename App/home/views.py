from django.shortcuts import render
from django.views import View
from django.db.models import Q
from user.models import Employee
from django.utils import timezone

class HomePage(View):
    def get(self, request):
        today = timezone.make_aware(timezone.make_naive(timezone.now()),timezone.get_current_timezone())
        month_ago = today - timezone.timedelta(days=30)
        new_joiners = Employee.objects.filter(Q(register_date__range=[month_ago,today]))
        context = {
            "new_joiners":  new_joiners
        }
        return render(request, 'home/homepage.html', context)
