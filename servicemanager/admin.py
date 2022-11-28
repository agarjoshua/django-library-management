from django.contrib import admin
import datetime
from django.utils import timezone
from .models import Author, Book, Issue, Service, ServiceType

# Register your models here.


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("employee", "book", "issued", "days_remaining")
    # list_filter=('issued')
    fields = ("employee", "book", ("issued", "returned"), "issued_at")
    search_fields = ["employee__employee_id__username", "book__name"]
    autocomplete_fields = ["employee", "book"]
    list_per_page = 30

    def days_remaining(self, obj):
        if obj.returned:
            return "returned"
        elif obj.return_date:
            y, m, d = str(timezone.now().date()).split("-")
            today = datetime.date(int(y), int(m), int(d))
            y2, m2, d2 = str(obj.return_date.date()).split("-")
            lastdate = datetime.date(int(y2), int(m2), int(d2))
            if lastdate > today:
                return f"{(lastdate - today).days} days"
            return f"{(today - lastdate).days} days passed"
        return "not issued"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "category")
    search_fields = ["name", "category"]
    list_filter = (("author", admin.RelatedOnlyFieldListFilter),)
    list_per_page = 30


class BookInline(admin.TabularInline):
    model = Book


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
    inlines = [
        BookInline,
    ]
    list_per_page = 30


@admin.register(ServiceType)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("type",)
    search_fields = ["type"]
    # inlines = [
    #     BookInline,
    # ]
    list_per_page = 30


# @admin.register(Service)
admin.site.register(Service)


class Service(admin.ModelAdmin):
    list_display = "employee"
    search_fields = ["employee", "type", "Department"]
    # inlines = [
    #     BookInline,
    # ]
    list_per_page = 30
