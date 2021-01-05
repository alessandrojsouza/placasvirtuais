from django.urls import path

from django.views.generic.base import RedirectView

from core import views

from core.views import DashboardView

app_name = 'core'
urlpatterns = [
  path(
    '',
    RedirectView.as_view(url='accounts/login', permanent=False),
    name='index'
  ),
  path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
