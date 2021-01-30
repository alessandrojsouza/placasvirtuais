from django.shortcuts import render

from rest_framework import generics

from vanilla import TemplateView
from vanilla import model_views as views
from django.utils.translation import ugettext as _

from board.serializers import BoardSerializer
from board.models import Board, Mentioned
from course.models import Course
from board.forms import BoardForm

from django.shortcuts import redirect


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
    # mentioned_obj = Mentioned.objects.get(pk=request.POST['mentioned'])

    board_obj = Board.objects.create(
      name=request.POST['name'],
      message=request.POST['message'],
      year_graduation=request.POST['year_graduation'],
      photo=self.request.FILES['photo'],
      graduation_date=request.POST['graduation_date'],
      course=course_obj,
      # mentioned=mentioned_obj
    )
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
    return redirect('/boards')

  def get_context_data(self, **kwargs):
    context = super(BoardUpdate, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    course = Course.objects.all().order_by('id')
    context.update({'courses': course})
    # mentioned = Mentioned.objects.all()
    # print("mentioned ------", mentioned)
    # context.update({'mentioneds': mentioned})
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
    board = Board.objects.all().order_by('id')
    context.update({'boards': board})
    return context
