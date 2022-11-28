from django.db import models
from user.models import Employee, Department
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=350)
    description = models.CharField(max_length=450)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=350)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField()
    category = models.CharField(max_length=220)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    type = models.CharField(max_length=350)


class Issue(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    issued = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return f"{self.employee}_{self.book} book issue request"


class Service(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee', null=False, default=1)
    type = models.CharField(max_length=220, default="Not applicable")
    details = models.CharField(max_length=220, default="Not applicable")
    pages = models.CharField(max_length=220, default="Not applicable")
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    file = models.FileField(default="Not applicable")
    created_at = models.DateTimeField(auto_now=True)
    issued = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return self.type
