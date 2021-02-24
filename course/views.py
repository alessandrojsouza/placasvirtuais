from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from rest_framework import generics

from vanilla import TemplateView
from vanilla import model_views as views
from django.utils.translation import ugettext as _

from course.serializers import CourseSerializer
from course.models import Course
from course.forms import CourseForm

from django.http import HttpResponseRedirect
from django.shortcuts import redirect



class LoginRequiredMixin(object):
  @classmethod
  def as_view(cls, **initkwargs):
    view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    return login_required(view)


class BaseCourseView(object):
  model = Course
  form_class = CourseForm
  lookup_field = 'pk'


# LoginRequiredMixin
class CourseApiView(generics.ListAPIView, generics.RetrieveAPIView,
                  generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
  queryset = Course.objects.all()
  serializer_class = CourseSerializer

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    queryset = super(CourseApiView, self).get_queryset()
    query = self.request.query_params.get('query', None)

    if query is not None:
      queryset = queryset.filter(name__icontains=query)

    if pk:
      queryset = queryset.filter(pk=pk)

    queryset = queryset.order_by('name')
    return queryset


class CourseList(BaseCourseView, views.ListView):
  template_name = 'course/list.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(CourseList, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    return context

  def get_queryset(self):
    queryset = super(CourseList, self).get_queryset()
    queryset = queryset.all().order_by('id', 'name')
    return queryset


class CourseCreate(BaseCourseView, views.CreateView):
  template_name = 'course/form.html'
  page_title = _(u'Add Course')

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect(
      self.object.get_update_url()
    )
  
  def post(self, request):
    course_obj = Course.objects.create(code=request.POST['code'], name=request.POST['name'])
    return redirect('/courses')


class CourseUpdate(BaseCourseView, views.UpdateView):
  template_name = 'course/form.html'

  def get_context_data(self, **kwargs):
    context = super(CourseUpdate, self).get_context_data(**kwargs)
    context.update(course_food_form=CourseForm())
    return context


class CoursePreview(BaseCourseView, views.UpdateView):
  template_name = 'course/preview.html'

  def get_context_data(self, **kwargs):
    context = super(CoursePreview, self).get_context_data(**kwargs)
    context.update(course_food_form=CourseForm())
    return context
