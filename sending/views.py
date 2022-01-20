from django.core.mail import send_mail
from django.utils.html import strip_tags
from sending.models import Sending
from sending.forms import SendingForm

from vanilla import model_views as views
from django.utils.translation import ugettext as _

from rest_framework import generics
from sending.serializers import SendingSerializer

from course.models import Course, Directorship
from board.models import Board

from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from sending.utils import get_recipient_list


class BaseSendingView(object):
    model = Sending
    form_class = SendingForm
    lookup_field = 'pk'


class SendingApiView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Sending.objects.all()
    serializer_class = SendingSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = super(SendingApiView, self).get_queryset()
        query = self.request.query_params.get('query', None)

        if query is not None:
            queryset = queryset.filter(subject__icontains=query)

        if pk:
            queryset = queryset.filter(pk=pk)

        queryset = queryset.order_by('subject')
        return queryset


class SendingList(BaseSendingView, views.ListView):
    template_name = 'sending/list.html'

    def get_context_data(self, **kwargs):
        context = super(SendingList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super(SendingList, self).get_queryset()
        queryset = queryset.all().order_by('id')
        return queryset


class SendingCreate(BaseSendingView, views.CreateView):
    template_name = 'sending/form.html'
    page_title = _(u'Add Sending')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(
            self.object.get_update_url()
        )
    
    def post(self, request):
        sender = self.request.user.email
        recipient_directorship = request.POST.getlist('recipient_directorship')
        recipient_board = request.POST.getlist('recipient_board')
        recipient_course = request.POST.getlist('recipient_course')
        recipient_year = request.POST['recipient_year']
        recipient_period = request.POST['recipient_period']
        subject = request.POST['subject']
        message = request.POST['message']

        egress_list = get_recipient_list(recipient_directorship, recipient_board, recipient_course, recipient_year, recipient_period)
        try:
            send_mail(
                subject=subject,
                message=strip_tags(message),
                from_email=sender,
                recipient_list=egress_list,
                fail_silently=False,
                html_message=message
            )

            Sending.objects.create(
                sender=sender,
                recipient=egress_list,
                subject=subject,
                message=message,
            )
            return redirect('/sending')
        except:
            print('Erro ao enviar email!')

    def get_context_data(self, **kwargs):
        context = super(SendingCreate, self).get_context_data(**kwargs)
        context.update(sending_food_form=SendingForm())
        course = Course.objects.all().order_by('id')
        boards = Board.objects.all().order_by('id')
        directorship = Directorship.objects.all().order_by('id')
        context.update({ 'boards': boards })
        context.update({ 'courses': course })
        context.update({ 'directories': directorship })
        context.update(name=self.request.GET.get('name', ''))
        return context


class SendingPreview(BaseSendingView, views.UpdateView):
  template_name = 'sending/preview.html'

  def get_context_data(self, **kwargs):
    context = super(SendingPreview, self).get_context_data(**kwargs)
    context.update(sending_food_form=SendingForm())
    course = Course.objects.all().order_by('id')
    boards = Board.objects.all().order_by('id')
    directorship = Directorship.objects.all().order_by('id')
    context.update({ 'boards': boards })
    context.update({ 'courses': course })
    context.update({ 'directories': directorship })
    context.update(name=self.request.GET.get('name', ''))
    return context
