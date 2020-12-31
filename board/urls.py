from django.urls import path

from board import views


app_name = 'board'
urlpatterns = [
  path(
    'api/',
    views.BoardApiView.as_view(),
    name='api_boards'
  ),
  path(
    'api/<int:pk>/',
    views.BoardApiView.as_view(),
    name='api_detail_boards'
  ),
]
