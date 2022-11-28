from django.contrib import admin
from .models import Employee,Department
from servicemanager.admin import IssueInline

from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(User)
admin.site.unregister(Group)
class EmployeeInline(admin.TabularInline):
    model = Employee
    
# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display=('username','employee','last_login')
    list_filter=('is_superuser','is_active')
    fieldsets =  (
      ('Standard info', {
          'fields': ('username','password',)
      }),
      ('Important Date & Time ', {
          'fields': ('last_login','date_joined',)
      }),)
    inlines = [
        EmployeeInline
    ]
      
   


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    search_fields=['employee_id__username','first_name','department']
    fields=(('first_name','last_name'),('staff_id','department'))
    list_display=('first_name','last_name','staff_id','department')
    list_display_links = ('first_name', 'staff_id')
    list_filter=('department__name',)
    list_per_page=30
    inlines = [
        IssueInline
    ]
    
admin.site.register(Department)
