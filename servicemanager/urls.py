from django.urls import path
from .views import (
    addrequest,
    allbooks,
    approverequest,
    delete_request,
    search,
    addrequest,
    request,
    issuerequest,
    myissues,
    issue_book,
    requestedissues,
    sort,
)

urlpatterns = [
    path("", allbooks, name="home"),
    path("search/", search),
    path("sort/", sort),
    path("addrequest/", addrequest),
    path("requests/", request),
    path("approve/<int:issueid>/", approverequest),
    path("deleterequest/<int:issueid>/", delete_request),
    path("request-book-issue/<int:bookID>/", issuerequest),
    path("my-issues/", myissues),
    path("all-issues/", requestedissues),
    path("issuebook/<int:issueID>/", issue_book),
]
