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
  path(
    'mentioned/api/<int:pk>/',
    views.MentionedApiView.as_view(),
    name='api_detail_boards'
  ),
  path(
    '',
    views.BoardList.as_view(),
    name='list'
  ),
  path(
    'create/',
    views.BoardCreate.as_view(),
    name='create'
  ),
  path(
    '<int:pk>/update/',
    views.BoardUpdate.as_view(),
    name='update'
  ),
  path(
    '<int:pk>/preview/',
    views.BoardPreview.as_view(),
    name='preview'
  ),
  path(
    '<int:pk>/preview-extern/',
    views.BoardPreview.as_view(),
    name='extern'
  ),
]
