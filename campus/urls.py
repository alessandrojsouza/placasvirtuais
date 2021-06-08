from django.urls import path

from campus import views


app_name = 'campus'
urlpatterns = [
  path(
    'api/',
    views.CampusApiView.as_view(),
    name='api_campus'
  ),
  path(
    'api/<int:pk>/',
    views.CampusApiView.as_view(),
    name='api_detail_campus'
  ),
  path(
    '',
    views.CampusList.as_view(),
    name='list'
  ),
  path(
    'create/',
    views.CampusCreate.as_view(),
    name='create'
  ),
  path(
    '<int:pk>/update/',
    views.CampusUpdate.as_view(),
    name='update'
  ),
  path(
    '<int:pk>/preview/',
    views.CampusPreview.as_view(),
    name='preview'
  ),
]
