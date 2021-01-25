from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from rest_framework import generics

from vanilla import TemplateView
from vanilla import model_views as views
from django.utils.translation import ugettext as _

from egress.serializers import EgressSerializer
from egress.models import Egress
from board.models import Board
from egress.forms import EgressForm

from django.http import HttpResponseRedirect
from django.shortcuts import redirect


class LoginRequiredMixin(object):
  @classmethod
  def as_view(cls, **initkwargs):
    view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    return login_required(view)


class BaseEgressView(object):
  model = Egress
  form_class = EgressForm
  lookup_field = 'pk'


# LoginRequiredMixin
class EgressApiView(generics.ListAPIView, generics.RetrieveAPIView,
                  generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
  queryset = Egress.objects.all()
  serializer_class = EgressSerializer

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    queryset = super(EgressApiView, self).get_queryset()
    query = self.request.query_params.get('query', None)

    if query is not None:
      queryset = queryset.filter(name__icontains=query)

    if pk:
      queryset = queryset.filter(pk=pk)

    queryset = queryset.order_by('name')
    return queryset


class EgressList(BaseEgressView, views.ListView):
  template_name = 'egress/list.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(EgressList, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    return context

  def get_queryset(self):
    queryset = super(EgressList, self).get_queryset()
    queryset = queryset.all().order_by('id', 'name')
    return queryset


class EgressCreate(BaseEgressView, views.CreateView):
  template_name = 'egress/form.html'
  page_title = _(u'Add Egress')

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect(
      self.object.get_update_url()
    )
  
  def post(self, request):
    board_obj = Board.objects.get(pk=request.POST['board'])
    print("board_obj", board_obj.pk)

    egress_obj = Egress.objects.create(
      enrollment=request.POST['enrollment'],
      name=request.POST['name'],
      email=request.POST['email'],
      social_network=request.POST['socialNetwork'],
      lattes=request.POST['lattes'],
      board=board_obj,
    )
    return redirect('/egress')

  def get_context_data(self, **kwargs):
    context = super(EgressCreate, self).get_context_data(**kwargs)
    context.update(egress_food_form=EgressForm())
    board = Board.objects.all().order_by('id')
    context.update({'boards': board})
    return context


class EgressUpdate(BaseEgressView, views.UpdateView):
  template_name = 'egress/form.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(EgressUpdate, self).get_context_data(**kwargs)
    # context.update(egress_food_form=EgressForm())
    context.update(name=self.request.GET.get('name', ''))
    board = Board.objects.all().order_by('id')
    context.update({'boards': board})
    return context

  def get_queryset(self):
    queryset = super(EgressUpdate, self).get_queryset()
    queryset = queryset.all().order_by('id', 'name')
    return queryset


class EgressPreview(BaseEgressView, views.UpdateView):
  template_name = 'egress/preview.html'

  def get_context_data(self, **kwargs):
    context = super(EgressPreview, self).get_context_data(**kwargs)
    context.update(egress_food_form=EgressForm())
    board = Board.objects.all().order_by('id')
    context.update({'boards': board})
    return context
