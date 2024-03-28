from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import CalendarDay
from django.utils import timezone
import locale

locale.setlocale(locale.LC_ALL, '')

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events, weekday):
        events_per_day = events.filter(datetime__day=day).order_by('datetime')
        d = ''
        options = '''<select name="teams">
            <option value="BFS">BFS</option>
            <option value="DEVS">DEVS</option>
            <option value="optional">optional</option>
            <option value="All">All</option>
        </select>'''
        for event in events_per_day:
            time = timezone.localtime(event.datetime)
            if event.team == "BFS":
                d += f'<li class="bfs">BFS</li>'
                d += f'<input name="teams" value="BFS" hidden />'
            elif event.team == "DEVS":
                d += f'<li class="devs">DEVS</li>'
                d += f'<input name="teams" value="DEVS" hidden />'
            elif event.team == "optional":
                d += f'<li class="optional">Optional</li>'
                d += f'<input name="teams" value="optional" hidden />'
            elif event.team == "All":
                d += f'<li class="all">All</li>'
                d += f'<input name="teams" value="All" hidden />'

        if day != 0 and weekday not in [5,6]:
            if len(d) > 2:
                return f"<td><span class='date'>{day}</span><ul> {d} </ul><input name='days' value='{day}' hidden /></td>"
            else:
                return f"<td><span class='date'>{day}</span><ul>{options} </ul><input name='days' value='{day}' hidden /></td>"
        elif day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'
    
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d,events, weekday)
        return f'<tr> {week} </tr>'
    
    def formatmonth(self, withyear=True):
        events = CalendarDay.objects.filter(datetime__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        cal += f'<input name="month" value="{self.month}" hidden/>'
        cal += f'<input name="year" value="{self.year}" hidden/>'

        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'</table>'
        return cal 