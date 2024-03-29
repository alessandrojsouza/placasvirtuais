import json

from django.contrib.auth.decorators import login_required

from rest_framework import generics
from django.conf import settings

from vanilla import TemplateView
from vanilla import model_views as views
from django.utils.translation import ugettext as _

from course.serializers import CourseSerializer
from course.models import Course, Directorship
from course.forms import CourseForm, DirectorshipForm

from rest_framework.response import Response
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

  def post(self, request):
    data = json.loads(request.data)
    try:
      if len(Course.objects.filter(code=data['code'])) > 1:
        return Response(status=400)
      else:
        directorship_obj = Directorship.objects.get(pk=request.POST['directorship'])

        course = Course.objects.create(
          code=data['code'],
          name=data['name'],
          directorship=directorship_obj,
        )
        course.save()
    except Exception:
      return Response(status=400)
    else:
      return Response(status=200)


class CourseList(BaseCourseView, views.ListView):
  template_name = 'course/list.html'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(CourseList, self).get_context_data(**kwargs)
    context.update(name=self.request.GET.get('name', ''))
    context.update(TOKEN_SUAP_SECRET=settings.TOKEN_SUAP_SECRET)
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
    directorship_obj = Directorship.objects.get(pk=request.POST['directorship'])

    Course.objects.create(
      code=request.POST['code'],
      name=request.POST['name'],
      directorship=directorship_obj,
    )
    return redirect('/courses')
  
  def get_context_data(self, **kwargs):
    context = super(CourseCreate, self).get_context_data(**kwargs)
    context.update(directorship_food_form=DirectorshipForm())
    directorship = Directorship.objects.all().order_by('id')
    context.update({'directorships': directorship})
    return context


class CourseUpdate(BaseCourseView, views.UpdateView):
  template_name = 'course/form.html'

  def post(self, request, pk):
    print('Directorship -----', request.POST)
    directorship_obj = Directorship.objects.get(pk=request.POST['directorship'])
    course_obj = Course.objects.get(id=pk)

    course_obj.code = request.POST['code']
    course_obj.name = request.POST['name']
    course_obj.directorship = directorship_obj
    course_obj.save()
    return redirect('/courses')

  def get_context_data(self, **kwargs):
    context = super(CourseUpdate, self).get_context_data(**kwargs)
    context.update(course_food_form=CourseForm())
    context.update(name=self.request.GET.get('name', ''))
    directorship = Directorship.objects.all().order_by('id')
    context.update({'directorships': directorship})
    return context

  def get_queryset(self):
    queryset = super(CourseUpdate, self).get_queryset()
    queryset = queryset.all().order_by('id', 'name')
    return queryset


class CoursePreview(BaseCourseView, views.UpdateView):
  template_name = 'course/preview.html'

  def get_context_data(self, **kwargs):
    context = super(CoursePreview, self).get_context_data(**kwargs)
    context.update(course_food_form=CourseForm())
    return context
