from django.db import models

TEAM = [("BFS", "BFS"),
        ("DEVS","DEVS"),
        ("All", "All"),
        ("Optional", "Optional")]

class CalendarDay(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    datetime = models.DateTimeField(unique = True)
    team = models.CharField(choices=TEAM, max_length=50, blank=False, null=False)

    def __str__(self):
        return str(self.datetime)
