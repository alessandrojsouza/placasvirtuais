import json

from django.shortcuts import render

from django.conf import settings

from django.contrib.auth.decorators import login_required

from rest_framework import generics

from rest_framework.response import Response

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen

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
    
  def post(self, request):
    data = json.loads(request.data)

    try:
      board_obj = Board.objects.get(pk=data['board'])

      egress = Egress.objects.create(
        name=data['name'],
        enrollment=data['enrollment'],
        lattes=data['lattes'],
        email=data['email'],
        board=board_obj
      )
      
      if data['photo'] != "":
        photo_url = data['photo']
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(photo_url).read())
        img_temp.flush()

        egress.photo.save("egress_%s.png" % egress.pk, File(img_temp))
        egress.save()
      egress.save()
    except Exception:
      return Response(status=400)
    else:
      return Response(status=200)


class EgressList(BaseEgressView, views.ListView):
  template_name = 'egress/list.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(EgressList, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    context.update(TOKEN_SUAP_SECRET=settings.TOKEN_SUAP_SECRET)
    board = Board.objects.all().order_by('id')
    context.update({'boards': board})
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

    egress_obj = Egress.objects.create(
      enrollment=request.POST['enrollment'],
      name=request.POST['name'],
      email=request.POST['email'],
      social_network=request.POST['socialNetwork'],
      photo=self.request.FILES['photo'],
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

  def post(self, request, pk):
    board_obj = Board.objects.get(pk=request.POST['board'])
    egreess_obj = Egress.objects.get(id=pk)
    
    if self.request.FILES:
      egreess_obj.photo = self.request.FILES['photo']

    egreess_obj.name = request.POST['name']
    egreess_obj.email = request.POST['email']
    egreess_obj.social_network = request.POST['socialNetwork']
    egreess_obj.lattes = request.POST['lattes']
    egreess_obj.board = board_obj
    egreess_obj.save()
    return redirect('/egress')

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
