from django.urls import path

from sending import views


app_name = 'sending'
urlpatterns = [
    path(
        '',
        views.SendingList.as_view(),
        name='list'
    ),
]
