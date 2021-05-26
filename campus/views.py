import json

from django.contrib.auth.decorators import login_required

from rest_framework import generics
from django.conf import settings

from vanilla import TemplateView
from vanilla import model_views as views
from django.utils.translation import ugettext as _

from campus.serializers import CampusSerializer
from campus.models import Campus
from campus.forms import CampusForm

from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect



class LoginRequiredMixin(object):
  @classmethod
  def as_view(cls, **initkwargs):
    view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    return login_required(view)


class BaseCampusView(object):
  model = Campus
  form_class = CampusForm
  lookup_field = 'pk'


# LoginRequiredMixin
class CampusApiView(generics.ListAPIView, generics.RetrieveAPIView,
                  generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
  queryset = Campus.objects.all()
  serializer_class = CampusSerializer

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    queryset = super(CampusApiView, self).get_queryset()
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
      if len(Campus.objects.filter(abbreviation=data['abbreviation'])) > 1:
        return Response(status=400)
      else:
        campus = Campus.objects.create(abbreviation=data['abbreviation'], name=data['name'])
        campus.save()
    except Exception:
      return Response(status=400)
    else:
      return Response(status=200)


class CampusList(BaseCampusView, views.ListView):
  template_name = 'campus/list.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(CampusList, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    context.update(TOKEN_SUAP_SECRET=settings.TOKEN_SUAP_SECRET)
    return context

  def get_queryset(self):
    queryset = super(CampusList, self).get_queryset()
    queryset = queryset.all().order_by('id', 'name')
    return queryset


class CampusCreate(BaseCampusView, views.CreateView):
  template_name = 'campus/form.html'
  page_title = _(u'Add Campus')

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect(
      self.object.get_update_url()
    )
  
  def post(self, request):
    Campus.objects.create(abbreviation=request.POST['abbreviation'], name=request.POST['name'])
    return redirect('/campus')


class CampusUpdate(BaseCampusView, views.UpdateView):
  template_name = 'campus/form.html'

  def get_context_data(self, **kwargs):
    context = super(CampusUpdate, self).get_context_data(**kwargs)
    context.update(campus_food_form=CampusForm())
    return context


class CampusPreview(BaseCampusView, views.UpdateView):
  template_name = 'campus/preview.html'

  def get_context_data(self, **kwargs):
    context = super(CampusPreview, self).get_context_data(**kwargs)
    context.update(campus_food_form=CampusForm())
    return context
