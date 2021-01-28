from django.shortcuts import render

from rest_framework import generics

from vanilla import TemplateView
from vanilla import model_views as views
from django.utils.translation import ugettext as _

from board.serializers import BoardSerializer
from board.models import Board
from board.forms import BoardForm

class BaseBoardView(object):
  model = Board
  form_class = BoardForm
  lookup_field = 'pk'


class BoardApiView(generics.ListAPIView, generics.RetrieveAPIView,
                  generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
  queryset = Board.objects.all()
  serializer_class = BoardSerializer

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    queryset = super(BoardApiView, self).get_queryset()
    query = self.request.query_params.get('query', None)

    if query is not None:
      queryset = queryset.filter(name__icontains=query)

    if pk:
      queryset = queryset.filter(pk=pk)

    queryset = queryset.order_by('name')
    return queryset


class BoardList(BaseBoardView, views.ListView):
  template_name = 'board/list.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(BoardList, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    return context

  def get_queryset(self):
    queryset = super(BoardList, self).get_queryset()
    queryset = queryset.all().order_by('id', 'name')
    return queryset
