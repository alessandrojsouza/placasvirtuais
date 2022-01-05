from django.urls import path

from emails import views


app_name = 'emails'
urlpatterns = [
    path(
        '',
        views.EmailList.as_view(),
        name='list'
    ),
]
