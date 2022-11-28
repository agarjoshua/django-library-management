from django.shortcuts import render, redirect
from .models import Book, Author, Issue, Service, ServiceType
from user.models import Department
from servicemanager.models import Book, Employee
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
import datetime
from .utilities import getmybooks
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
from core import settings


# Book
def allbooks(request):
    requestedbooks, issuedbooks = getmybooks(request.user)
    allbooks = Book.objects.all()

    return render(
        request,
        "servicemanager/home.html",
        {
            "books": allbooks,
            "issuedbooks": issuedbooks,
            "requestedbooks": requestedbooks,
        },
    )


def sort(request):
    sort_type = request.GET.get("sort_type")
    sort_by = request.GET.get("sort")
    requestedbooks, issuedbooks = getmybooks(request.user)
    if "author" in sort_type:
        author_results = Author.objects.filter(name__startswith=sort_by)
        return render(
            request,
            "servicemanager/home.html",
            {
                "author_results": author_results,
                "issuedbooks": issuedbooks,
                "requestedbooks": requestedbooks,
                "selected": "author",
            },
        )
    else:
        books_results = Book.objects.filter(name__startswith=sort_by)
        return render(
            request,
            "servicemanager/home.html",
            {
                "books_results": books_results,
                "issuedbooks": issuedbooks,
                "requestedbooks": requestedbooks,
                "selected": "book",
            },
        )


def search(request):
    search_query = request.GET.get("search-query")
    search_by_author = request.GET.get("author")
    requestedbooks, issuedbooks = getmybooks(request.user)

    if search_by_author is not None:
        author_results = Author.objects.filter(name__icontains=search_query)
        return render(
            request,
            "servicemanager/home.html",
            {
                "author_results": author_results,
                "issuedbooks": issuedbooks,
                "requestedbooks": requestedbooks,
            },
        )
    else:
        books_results = Book.objects.filter(
            Q(name__icontains=search_query) | Q(category__icontains=search_query)
        )
        return render(
            request,
            "servicemanager/home.html",
            {
                "books_results": books_results,
                "issuedbooks": issuedbooks,
                "requestedbooks": requestedbooks,
            },
        )


@login_required(login_url="/employee/login/")
def addrequest(request):
    department = Employee.objects.get(staff_id=request.user).department
    test = Employee.objects.all()
    service_type = ServiceType.objects.all()

    if request.method == "POST":
        department = Employee.objects.filter(staff_id=request.user)
        details = request.POST.get("details")
        pages = request.POST.get("pages")
        file = request.FILES.get("file")
        type = request.POST.get("service")
        print("---------------------------------------------")
        print(type)
        print("---------------------------------------------")

        try:
            test = Service.objects.create(
                employee=request.user,
                type=request.POST["service"],
                details=details,
                pages=pages,
                Department=Employee.objects.get(staff_id=request.user).department,
                file=file,
            )
        except:
            print("catch")

        messages.success(request, f"Request Added succesfully")
        return render(
            request,
            "servicemanager/addrequest.html",
            # {'authors': authors,}
        )

    else:
        return render(
            request,
            "servicemanager/addrequest.html",
            {
                # 'authors': authors,
                "service_type": service_type
            },
        )


@login_required(login_url="/employee/login/")
@user_passes_test(lambda u: u.is_superuser, login_url="/employee/login/")
def deletebook(request, bookID):
    book = Book.objects.get(id=bookID)
    messages.success(request, f"Book - {book.name} Deleted succesfully ")
    book.delete()
    return redirect("/")


#  ISSUES
def request(request):
    issues = Service.objects.all()
    print(issues)
    return render(request, "servicemanager/requests.html", {"issues": issues})


# approval function
# @user_passes_test(lambda u: not u.is_superuser, login_url='/employee/login/')


def delete_request(request, issueid):
    issues = Service.objects.all()
    old_issue = Service.objects.get(id=issueid)
    print(old_issue)
    old_issue.delete()
    return render(request, "servicemanager/requests.html", {"issues": issues})


# def approve_request(request, issueid):
# issues = Service.objects.all()
# old_issue = Service.objects.get(id=issueid)
# print(old_issue)
# old_issue.update(issued=True)
# return render(request,'servicemanager/requests.html', {"issues" : issues})


@login_required(login_url="/admin/")
@user_passes_test(lambda u: u.is_superuser, login_url="/employee/login/")
def approverequest(request, issueid):
    issues = Service.objects.all()
    service = Service.objects.get(id=issueid)

    service.return_date = timezone.now() + datetime.timedelta(days=15)
    service.issued_at = timezone.now()
    service.issued = True
    service.save()
    return render(request, "servicemanager/requests.html", {"issues": issues})


@login_required(login_url="/employee/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/employee/login/")
def issuerequest(request, bookID):

    employee = Employee.objects.get(staff_id=request.user)
    print(employee)
    if employee:
        book: str = Book.objects.get(id=bookID)
        issue, created = Issue.objects.get_or_create(book=book, employee=employee)
        print(issue, created)
        messages.success(request, f"Book - {book.name} Requested succesfully")
        return redirect("home")

    messages.error(request, "You are Not a employee !")

    return redirect("/")


@login_required(login_url="/employee/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/employee/login/")
def myissues(request):
    if Employee.objects.filter(staff_id=request.user):
        # employee = employee.objects.filter(staff_id=request.user)[0]
        issues = Service.objects.filter(employee=request.user)
        print(issues)

        # if request.GET.get('issued') is not None:
        #     issues = Issue.objects.filter(employee=employee, issued=True)
        # elif request.GET.get('notissued') is not None:
        #     issues = Issue.objects.filter(employee=employee, issued=False)
        # else:
        #     issues = Issue.objects.filter(employee=employee)

        return render(request, "servicemanager/myissues.html", {"issues": issues})

    messages.error(request, "You are Not a employee !")
    return redirect("/")


@login_required(login_url="/admin/")
@user_passes_test(lambda u: u.is_superuser, login_url="/admin/")
def requestedissues(request):
    if (
        request.GET.get("employeeID") is not None
        and request.GET.get("employeeID") != ""
    ):
        try:
            user = User.objects.get(username=request.GET.get("employeeID"))
            employee = Employee.objects.filter(staff_id=user)
            if employee:
                employee = employee[0]
                issues = Issue.objects.filter(employee=employee, issued=False)
                return render(
                    request, "servicemanager/allissues.html", {"issues": issues}
                )
            messages.error(request, "No employee found")
            return redirect("/all-issues/")
        except User.DoesNotExist:
            messages.error(request, "No employee found")
            return redirect("/all-issues/")

    else:
        issues = Issue.objects.filter(issued=False)
        return render(request, "servicemanager/allissues.html", {"issues": issues})


@login_required(login_url="/admin/")
@user_passes_test(lambda u: u.is_superuser, login_url="/employee/login/")
def issue_book(request, issueID):
    issue = Issue.objects.get(id=issueID)
    issue.return_date = timezone.now() + datetime.timedelta(days=15)
    issue.issued_at = timezone.now()
    issue.issued = True
    issue.save()
    return redirect("/all-issues/")
