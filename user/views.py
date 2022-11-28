import sqlite3
from django.shortcuts import render, redirect
from .models import Employee, Department, Employee
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages


def logout(request):
    auth.logout(request)
    messages.success(request, "Logout successful")
    return redirect("home")


def login(request):
    if request.method != "POST":
        return render(request, "employee/login.html")
    user = auth.authenticate(
        request,
        username=request.POST["studentID"],
        password=request.POST["password"],
    )

    print(user)
    if user is None:
        messages.error(request, "Invalid CREDENTIALS")
        return redirect("/employee/login/")
    else:
        auth.login(request, user)
        messages.success(request, "Login successful")
        if "next" in request.POST:
            return redirect(request.POST["next"])
        return redirect("home")


def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["studentID"])
            messages.success(request, "user exists already !!")
            return redirect("/employee/login/")

        # except (sqlite3.IntegrityError) as e:
        #     print('---------------------------------------------------')
        #     print(e)
        #     print('---------------------------------------------------')
        #     messages.success(request, 'user exists already !!')
        #     return redirect('/employee/signup/')

        except User.DoesNotExist:
            print("---------------------------------------------------")
            user = User.objects.create(
                username=request.POST["studentID"], password=request.POST["password"]
            )
            print("---------------------------------------------------")
            newstaff = Employee.objects.create(
                first_name=request.POST["firstname"],
                last_name=request.POST["lastname"],
                department=Department.objects.get(id=request.POST["department"]),
                staff_id=user,
            )
            print("---------------------------------------------------")
            print(newstaff)
            print("---------------------------------------------------")

            auth.login(request, user)
            messages.success(request, "Signup successful")
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("home")

    else:
        return render(
            request,
            "employee/signup.html",
            {
                "departments": Department.objects.all(),
                "users": list(User.objects.values_list("username", flat=True)),
            },
        )
