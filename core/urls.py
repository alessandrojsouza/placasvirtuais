from django.urls import path

from django.views.generic.base import RedirectView

from core import views

from core.views import DashboardView, UserApiView, UserList, UserCreate, UserUpdate


app_name = 'core'
urlpatterns = [
  path(
    '',
    RedirectView.as_view(url='accounts/login', permanent=False),
    name='index'
  ),
  path('dashboard/', DashboardView.as_view(), name='dashboard'),
  path(
    'api/',
    UserApiView.as_view(),
    name='api_users'
  ),
  path(
    'api/<int:pk>/',
    UserApiView.as_view(),
    name='api_detail_users'
  ),
  path(
    'users/',
    UserList.as_view(),
    name='list'
  ),
  path(
    'users/create',
    UserCreate.as_view(),
    name='create'
  ),
  path(
    'user/<int:pk>/update/',
    UserUpdate.as_view(),
    name='update'
  ),
]
