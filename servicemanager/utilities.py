import datetime
from django.utils import timezone
from .models import Book
from user.models import Employee


def getmybooks(user):
    "Get issued books or requested books of a employee takes a user & returns a tuple"
    requestedbooks = []
    issuedbooks = []
    if user.is_authenticated:
        if employee := Employee.objects.filter(staff_id=user):
            for b in Book.objects.all():
                for i in b.issue_set.all():
                    if i.employee == employee[0]:
                        if i.issued:
                            issuedbooks.append(b)
                        else:
                            requestedbooks.append(b)
    return [requestedbooks, issuedbooks]


def accountant(user) -> int:
    """ "
    This calculates and returns the balance of vote that a 
    department has against all the services requested for

    Returns:
        str: Balance ammount that is left
    """
    pass
