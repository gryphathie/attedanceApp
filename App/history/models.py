from django.db import models

class History(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    personnel_id = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    card_number = models.CharField(max_length=20, blank=True, null=True)
    device_name = models.CharField(max_length=200, blank=True, null=True)
    event_point = models.CharField(max_length=200, blank=True, null=True)
    verify_type = models.CharField(max_length=100, blank=True, null=True)
    in_out_status = models.CharField(max_length=100, blank=True, null=True)
    event_description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.date_time)


class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.file_name)