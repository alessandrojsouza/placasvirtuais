from django.urls import path

from sending import views


app_name = 'sending'
urlpatterns = [
    path(
        'api/',
        views.SendingApiView.as_view(),
        name='api_sending'
    ),
    path(
        'api/<int:pk>/',
        views.SendingApiView.as_view(),
        name='api_detail_sending'
    ),
    path(
        '',
        views.SendingList.as_view(),
        name='list'
    ),
    path(
        'create/',
        views.SendingCreate.as_view(),
        name='create'
    ),
    path(
        '<int:pk>/preview/',
        views.SendingPreview.as_view(),
        name='preview'
    ),
]
