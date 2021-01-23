from django.urls import path

from egress import views


app_name = 'egress'
urlpatterns = [
  path(
    'api/',
    views.EgressApiView.as_view(),
    name='api_egress'
  ),
  path(
    'api/<int:pk>/',
    views.EgressApiView.as_view(),
    name='api_detail_egress'
  ),
  path(
    '',
    views.EgressList.as_view(),
    name='list'
  ),
  path(
    'create/',
    views.EgressCreate.as_view(),
    name='create'
  ),
  path(
    '<int:pk>/update/',
    views.EgressUpdate.as_view(),
    name='update'
  ),
  path(
    '<int:pk>/preview/',
    views.EgressPreview.as_view(),
    name='preview'
  ),
]
