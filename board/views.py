from django.shortcuts import render
from django.db import models

from rest_framework import generics, filters

from vanilla import TemplateView
from vanilla import model_views as views
from django.utils.translation import ugettext as _

from board.serializers import BoardSerializer, MentionedSerializer

from board.models import Board, Mentioned
from course.models import Course
from egress.models import Egress

from board.forms import BoardForm

from django.shortcuts import redirect


class BaseBoardView(object):
  model = Board
  form_class = BoardForm
  lookup_field = 'pk'


class BoardApiView(generics.ListAPIView, generics.RetrieveAPIView,
                  generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):  
  search_fields = ['name', 'course__name', 'course__id']
  filter_backends = (filters.SearchFilter,)

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


class MentionedApiView(generics.ListAPIView, generics.RetrieveAPIView,
                  generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
  queryset = Mentioned.objects.all()
  serializer_class = MentionedSerializer

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    queryset = super(MentionedApiView, self).get_queryset()
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
    course = Course.objects.all().order_by('id')
    context.update({'courses': course})
    context.update(name=self.request.GET.get('name', ''))
    return context

  def get_queryset(self):
    queryset = super(BoardList, self).get_queryset()
    search_name = self.request.GET.get('name', '')
    search_course = self.request.GET.get('course', '')

    if search_name is not None:
      queryset = queryset.filter(
        models.Q(name__icontains=search_name)
      )
    if search_course is not None:
      queryset = queryset.filter(
        models.Q(course__id__icontains=search_course)
      )

    queryset = queryset.all().order_by('id', 'name')
    return queryset


class BoardCreate(BaseBoardView, views.CreateView):
  template_name = 'board/form.html'
  page_title = _(u'Add Board')

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect(
      self.object.get_update_url()
    )
  
  def post(self, request):
    course_obj = Course.objects.get(pk=request.POST['course'])
  
    board_obj = Board.objects.create(
      name=request.POST['name'],
      message=request.POST['message'],
      year_graduation=request.POST['year_graduation'],
      photo=self.request.FILES['photo'],
      graduation_date=request.POST['graduation_date'],
      course=course_obj,
    )

    values = [value for name, value in self.request.POST.items()
      if name != 'name' and name != 'year_graduation' and name != 'graduation_date' and name != 'csrfmiddlewaretoken' and name != 'period_graduation' and name != 'date' and name != 'course' and name != 'message'
    ]
    for name, mention in zip(values[::2], values[1::2]):
      mentioned_obj_new = Mentioned.objects.create(
        name=name,
        mention=mention
      )
      board_obj.mentioned.add(mentioned_obj_new)
    return redirect('/boards')

  def get_context_data(self, **kwargs):
    context = super(BoardCreate, self).get_context_data(**kwargs)
    context.update(egress_food_form=BoardForm())
    course = Course.objects.all().order_by('id')
    context.update({'courses': course})
    mentioned = Mentioned.objects.all()
    context.update({'mentioneds': mentioned})
    return context

class BoardUpdate(BaseBoardView, views.UpdateView):
  template_name = 'board/form.html'
  paginate_by = 25

  # FIXME: update mentioneds objs
  def post(self, request, pk):
    course_obj = Course.objects.get(pk=request.POST['course'])
    board_obj = Board.objects.get(id=pk)
    
    if self.request.FILES:
      board_obj.photo = self.request.FILES['photo']

    board_obj.name = request.POST['name']
    board_obj.year_graduation = request.POST['year_graduation']
    board_obj.graduation_date = request.POST['graduation_date']
    board_obj.message = request.POST['message']
    board_obj.course = course_obj
    board_obj.save()
    return redirect('/boards')

  def get_context_data(self, **kwargs):
    context = super(BoardUpdate, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    course = Course.objects.all().order_by('id')
    context.update({'courses': course})
    board_obj = Board.objects.get(pk=self.kwargs.get('pk'))
    return context

  def get_queryset(self):
    queryset = super(BoardUpdate, self).get_queryset()
    queryset = queryset.all().order_by('id', 'name')
    return queryset


class BoardPreview(BaseBoardView, views.UpdateView):
  template_name = 'board/preview.html'

  def get_context_data(self, **kwargs):
    context = super(BoardPreview, self).get_context_data(**kwargs)
    context.update(board_food_form=BoardForm())
    course = Course.objects.all().order_by('id')
    context.update({'courses': course})
    mentioned = Mentioned.objects.all()
    context.update({'mentioneds': mentioned})
    return context


class BoardPreviewExtern(BaseBoardView, views.UpdateView):
  template_name = 'board/preview_extern.html'

  def get_context_data(self, **kwargs):
    context = super(BoardPreviewExtern, self).get_context_data(**kwargs)
    context.update(board_food_form=BoardForm())
    course = Course.objects.all().order_by('id')
    context.update({'courses': course})
    mentioned = Mentioned.objects.all()
    context.update({'mentioneds': mentioned})
    egress = Egress.objects.filter(board=self.kwargs.get('pk'))
    context.update({'egress': egress})
    return context
