import json

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import generics

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen

from vanilla import TemplateView
from vanilla import model_views as views
from django.utils.translation import ugettext as _

from django.db import models

from core.serializers import UserSerializer

from core.models import User
from course.models import Course
from board.models import Board
from egress.models import Egress

from core.forms import UserForm
from board.forms import BoardForm

from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from django.contrib import auth
from .oauth2 import OAuth2Response


class LoginRequiredMixin(object):
  @classmethod
  def as_view(cls, **initkwargs):
    view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    return login_required(view)


class BaseUserView(object):
  model = User
  form_class = UserForm
  lookup_field = 'pk'

class BaseBoardView(object):
  model = Board
  form_class = BoardForm
  lookup_field = 'pk'


class DashboardView(LoginRequiredMixin, TemplateView):
  template_name = 'dashboard.html'


class UserApiView(generics.ListAPIView, generics.RetrieveAPIView,
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

  def post(self, request):
    data = json.loads(request.data)

    try:
      user = User.objects.create_user(data['username'], data['email'], 'admin2@ifrn')
      user.first_name = data['firstname']
      
      if data['avatar'] != "":
        avatar_url = data['avatar']
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(avatar_url).read())
        img_temp.flush()

        user.avatar.save("avatar_%s.png" % user.pk, File(img_temp))
        user.save()
      user.save()
    except Exception:
      return Response(status=400)
    else:
      return Response(status=200)


class UserList(BaseUserView, views.ListView):
  template_name = 'list.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(UserList, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    context.update(TOKEN_SUAP_SECRET=settings.TOKEN_SUAP_SECRET)
    return context

  def get_queryset(self):
    queryset = super(UserList, self).get_queryset()
    queryset = queryset.filter(is_staff=False).order_by('id', 'username')
    return queryset


class UserCreate(BaseUserView, views.CreateView):
  template_name = 'form.html'
  page_title = _(u'Add User')

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect(
      self.object.get_update_url()
    )
  
  def post(self, request):
    name = request.POST['name'].split(" ")
    print("name -------------------", name)
    
    user = User.objects.create_user(request.POST['username'], request.POST['email'], 'admin2@ifrn')
    # Update fields and then save again
    user.first_name = name[0]
    user.last_name = name[1]
    user.save()
    return redirect('/users')

  # def get_context_data(self, **kwargs):
  #   context = super(UserCreate, self).get_context_data(**kwargs)
  #   # context.update(user_food_form=DietFoodForm())
  #   return context

  # def dispatch(self, *args, **kwargs):
  #   return super(UserCreate, self).dispatch(*args, **kwargs)


class UserUpdate(BaseUserView, views.UpdateView):
  template_name = 'form.html'

  def get_context_data(self, **kwargs):
    context = super(UserUpdate, self).get_context_data(**kwargs)
    context.update(user_food_form=UserForm())
    return context


class UserPreview(BaseUserView, views.UpdateView):
  template_name = 'preview.html'

  def get_context_data(self, **kwargs):
    context = super(UserPreview, self).get_context_data(**kwargs)
    context.update(user_food_form=UserForm())
    return context


class PageExtern(BaseBoardView, views.ListView):
  template_name = 'extern.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(PageExtern, self).get_context_data(**kwargs)
    course = Course.objects.all().order_by('id')
    context.update({'courses': course})
    context.update(name=self.request.GET.get('name', ''))
    return context

  def get_queryset(self):
    queryset = super(PageExtern, self).get_queryset()
    search_name = self.request.GET.get('name', None)
    search_year = self.request.GET.get('year', None)
    search_period = self.request.GET.get('period', None)
    search_course = self.request.GET.get('course', None)

    if search_name is not None:
      egress = Egress.objects.filter(name__icontains=search_name)
      if egress:
        for item in egress:
          queryset = queryset.filter(
            models.Q(name__icontains=item.board)
          )
      else:
        queryset = queryset.filter(
          models.Q(name__icontains='@')
        )

    if search_year is not None:
      queryset = queryset.filter(
        models.Q(year_graduation__icontains=search_year)
      )

    if search_period is not None:
      queryset = queryset.filter(
        models.Q(period_graduation__icontains=search_period)
      )

    if search_course is not None:
      queryset = queryset.filter(
        models.Q(course__id__icontains=search_course)
      )

    queryset = queryset.all().order_by('id', 'name')
    return queryset


def suap_login(request):
  response = OAuth2Response(request)
  if response.data:
    user = User.objects.filter(email=response.data.get('email_secundario')).first()
    if user:
      auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
      return HttpResponseRedirect('/dashboard/')
    else:
      return HttpResponseRedirect('/?status=error')
  return response


class PageExternDiretory(BaseBoardView, views.ListView):
  template_name = 'diretory.html'

  def get_context_data(self, **kwargs):
    context = super(PageExternDiretory, self).get_context_data(**kwargs)
    context.update(name=self.kwargs.get('diretory').capitalize())
    return context

  def get_queryset(self):
    queryset = super(PageExternDiretory, self).get_queryset()
    diretory_name = self.request.GET.get('diretory', None)

    if diretory_name is not None:
      egress = Egress.objects.filter(name__icontains=diretory_name)
      if egress:
        for item in egress:
          queryset = queryset.filter(
            models.Q(name__icontains=item.board)
          )
      else:
        queryset = queryset.filter(
          models.Q(name__icontains='@')
        )

    queryset = queryset.all().order_by('id', 'name')
    return queryset
