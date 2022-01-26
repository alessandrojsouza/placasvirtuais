from django.core.mail import send_mail, EmailMessage
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
        egress_list_count = len(egress_list)

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=sender,
                to=egress_list
            )
            email.content_subtype = "html"
            
            if self.request.FILES:
                file = self.request.FILES['file']
                email.attach(file.name, file.read(), file.content_type)
            email.send()

            sending_obj = Sending.objects.create(
                sender=sender,
                recipient_year=recipient_year,
                recipient_period=recipient_period,
                recipient_count=egress_list_count,
                subject=subject,
                message=message,
            )
            if recipient_directorship:
                for directorship in recipient_directorship:
                    directorship_obj = Directorship.objects.get(
                        pk=directorship
                    )
                    sending_obj.recipient_directorship.add(directorship_obj)

            if recipient_board:
                for board in recipient_board:
                    board_obj = Board.objects.get(
                        pk=board
                    )
                    sending_obj.recipient_board.add(board_obj)

            if recipient_course:
                for course in recipient_course:
                    course_obj = Course.objects.get(
                        pk=course
                    )
                    sending_obj.recipient_course.add(course_obj)

            if self.request.FILES:
                sending_obj.file = self.request.FILES['file']
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
