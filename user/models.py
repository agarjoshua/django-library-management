from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=200)
    vote=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    staff_id=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=120)
    last_name=models.CharField(max_length=120)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        last_4_digits=self.staff_id.username[-4:]
        return f"{self.first_name}_{last_4_digits}-{self.department}"
        # return self.id
    

    