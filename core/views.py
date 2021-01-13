from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from rest_framework import generics

from vanilla import TemplateView
from vanilla import model_views as views

from core.serializers import UserSerializer
from core.models import User
from core.forms import UserForm


class LoginRequiredMixin(object):
  @classmethod
  def as_view(cls, **initkwargs):
    view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    return login_required(view)


class BaseUserView(object):
  model = User
  form_class = UserForm
  lookup_field = 'pk'


class DashboardView(LoginRequiredMixin, TemplateView):
  template_name = 'dashboard.html'


class UserApiView(LoginRequiredMixin, generics.ListAPIView, generics.RetrieveAPIView,
                  generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    queryset = super(UserApiView, self).get_queryset()
    query = self.request.query_params.get('query', None)

    if query is not None:
      queryset = queryset.filter(username__icontains=query)

    if pk:
      queryset = queryset.filter(pk=pk)

    queryset = queryset.order_by('username')
    return queryset


class UserList(BaseUserView, views.ListView):
  template_name = 'list.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(UserList, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    return context

  def get_queryset(self):
    queryset = super(UserList, self).get_queryset()
    queryset = queryset.all().order_by('id', 'username')

    return queryset
