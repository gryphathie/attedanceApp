from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from .forms import CsvForm, HistoryForm
from .models import Csv, History
from user.models import Employee, Leave, Guest
from django.db.models.query import Q
import pandas as pd
from datetime import datetime
from django.utils import timezone
import csv, xlrd

class CsvHistoryView(View):
    def get(self, request):
        form = CsvForm()
        template_name = 'history/import.html'
        return render(request, template_name, {'form':form})
    
    def post(self, request):
        template_name = 'history/import.html'
        form = CsvForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form = CsvForm()
            obj = Csv.objects.get(activated=False)            
            # with open(obj.file_name.path, 'r') as f:
            #     reader = csv.reader(f)
            #     for i, row in enumerate(reader):
            #         if i != 0:
            #             print(row)
            #             date_time = row[1]
            #             personnel_id = row[2]
            #             first_name = row[3]
            #             last_name = row[4]
            #             card_number = row[5]
            #             device_name = row[6]
            #             event_point = row[7]
            #             verify_type = row[8]
            #             in_out_status = row[9]
            #             event_description = row[10]
            #             History.objects.create(
            #                 date_time = date_time,
            #                 personnel_id = personnel_id,
            #                 first_name = first_name,
            #                 last_name = last_name,
            #                 card_number = card_number,
            #                 device_name = device_name,
            #                 event_point = event_point,
            #                 verify_type = verify_type,
            #                 in_out_status = in_out_status,
            #                 event_description = event_description,
            #             )
            try:
                ReadXLSFile(obj.file_name.path)
                obj.activated = True
                obj.save()
                messages.success(request, 'File successfully imported!')
            except Exception as e:
                messages.error(request, "Error at importing the file" + str(e))
            return render(request, template_name, {'form':form})
        else:
            messages.error(request, form.errors.as_ul())
            return render(request, template_name, {'form':form})


def ReadXLSFile(filename):
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_name('data')
    max_rows = worksheet.nrows
    for i in range(max_rows):
        if i != 0:
            if worksheet.cell(i,1) != '':
                date_time = worksheet.cell(i,0).value
                date = (date_time.split(" "))[0]
                time = ((date_time.split(" "))[1])
                personnel_id = str(worksheet.cell(i,1).value).replace(".0","")
                first_name = worksheet.cell(i,2).value
                last_name = worksheet.cell(i,3).value
                card_number = str(worksheet.cell(i,4).value).replace(".0","")
                device_name = worksheet.cell(i,5).value
                event_point = worksheet.cell(i,6).value
                verify_type = worksheet.cell(i,7).value
                in_out_status = worksheet.cell(i,8).value
                event_description = worksheet.cell(i,9).value                
                History.objects.create(
                    date = date,
                    time = time,
                    personnel_id = personnel_id,
                    first_name = first_name,
                    last_name = last_name,
                    card_number = card_number,
                    device_name = device_name,
                    event_point = event_point,
                    verify_type = verify_type,
                    in_out_status = in_out_status,
                    event_description = event_description,
                )


class SearchEmployeeAttendance(View):
    def get(self, request):
        form = HistoryForm()
        context = {
            'form': form,
        }
        return render(request, 'history/search_attendance.html', context)
    
    def post(self, request):
        form = HistoryForm(request.POST)   
        employee = None     
        history = None
        ace = None   
        leaves = None 
        guests = None     
        employee_name = request.POST.get('name')
        card_number = request.POST.get('card_number')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_from = timezone.make_aware(date_from, timezone.get_current_timezone())
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
        date_to = timezone.make_aware(date_to, timezone.get_current_timezone())        
        if employee_name != "":
            print("Normal ACE")
            employee = Employee.objects.get(name=employee_name)
            ace = str(employee.ace)
            leaves = Leave.objects.filter(
                Q(employee__in=[employee]) &
                Q(start_date__range=[date_from, date_to])
            ).order_by('start_date')

            guests = Guest.objects.filter(
                Q(employee__in=[employee]) &
                Q(start_date__range=[date_from, date_to])
            ).order_by('start_date')            
            
            history = History.objects.filter(
                Q(personnel_id__in = [ace]) &                
                Q(date__range=[date_from, date_to])                       
            ).order_by('date', 'time') 

            #TODO: Crear otro history que sea exclusivo para las guest card y otra tabla en el template.
            #Haciendo uso de los card number y las fechas de inicio y fin viendo como juntarlos con el reporte.
            a = list()
            for guest in guests: a.append(guest.card_number)
            
            history = History.objects.filter(
                Q(personnel_id__in = [ace]) |
                Q(card_number__in=a) &
                Q(date__range=[date_from, date_to])                       
            ).order_by('date', 'time')


        elif card_number != "":
            print("Normal CARD")
            employee = Employee.objects.filter(Q(card_number1__icontains=card_number) | Q(card_number2__icontains=card_number) | Q(card_number3__icontains=card_number)).first()
            history = History.objects.filter(
                Q(card_number__in=[card_number]) &
                Q(date__range=[date_from, date_to])                       
            ).order_by('date', 'time')  

            leaves = Leave.objects.filter(
                Q(employee__in=[employee]) &
                Q(start_date__range=[date_from, date_to])
            ).order_by('start_date')

            guests = Guest.objects.filter(
                Q(employee__in=[employee]) &
                Q(start_date__range=[date_from, date_to])
            ).order_by('start_date')

        if "generate_report" in self.request.POST:
            print("Generate report")
            df = pd.DataFrame(list(history.values()))            
            a = df[['date','personnel_id','card_number','first_name']].drop_duplicates()
            print(a)

        context = {
            'form': form,
            'history': history,
            'leaves': leaves,
            'guests': guests,
        }
        return render(request, 'history/search_attendance.html', context)

