from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=15,unique=True)
    department = models.CharField(max_length=50)
    admission_date = models.DateField()
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"
   

