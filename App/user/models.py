from django.db import models

TEAM = [("BFS", "BFS"),
        ("DEVS", "DEVS")]

LEAVES = [("WFH", "WFH"),
          ("SL", "Sick"),
          ("VL", "Vacations"),
          ("BL", "Bereavement"),
          ("ML", "Maternity"),
          ("PL", "Paternity"),
          ("CL", "Compensatory")
          ]

class Employee(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=500, null=False)
    ace = models.CharField(max_length=30, null=False, blank=False, default="0001")
    card_number1 = models.CharField(max_length=20, null=False, blank=False)
    card_number2 = models.CharField(max_length=20, null=True, blank=True)
    card_number3 = models.CharField(max_length=20, null=True, blank=True)
    team = models.CharField(choices=TEAM, max_length=50, blank=False, null=False)
    register_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.name)
    

class Guest(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null = True, blank = True)

    def __str__(self):
        return str(self.employee.name)
    

class Leave(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    leave_type = models.CharField(choices=LEAVES, max_length=50, blank=False, null=False, default="VL")

    def __str__(self):
        return str(self.employee.name)