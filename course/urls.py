from django.urls import path

from course import views


app_name = 'course'
urlpatterns = [
  path(
    'api/',
    views.CourseApiView.as_view(),
    name='api_courses'
  ),
  path(
    'api/<int:pk>/',
    views.CourseApiView.as_view(),
    name='api_detail_courses'
  ),
  path(
    '',
    views.CourseList.as_view(),
    name='list'
  ),
  path(
    'create/',
    views.CourseCreate.as_view(),
    name='create'
  ),
  path(
    '<int:pk>/update/',
    views.CourseUpdate.as_view(),
    name='update'
  ),
  path(
    '<int:pk>/preview/',
    views.CoursePreview.as_view(),
    name='preview'
  ),
]
