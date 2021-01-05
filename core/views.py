from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from vanilla import TemplateView


class LoginRequiredMixin(object):
  @classmethod
  def as_view(cls, **initkwargs):
    view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    return login_required(view)


class DashboardView(LoginRequiredMixin, TemplateView):
  template_name = 'dashboard.html'
