from sending.models import Sending
from sending.forms import SendingForm

from vanilla import model_views as views
from django.utils.translation import ugettext as _

from django.http import HttpResponseRedirect
from django.shortcuts import redirect


class BaseSendingView(object):
    model = Sending
    form_class = SendingForm
    lookup_field = 'pk'


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
        # board_obj = Board.objects.get(pk=request.POST['board'])

        Sending.objects.create(
            sender=request.POST['sender'],
            subject=request.POST['subject'],
            message=request.POST['message'],
            #   board=board_obj,
        )
        return redirect('/sending')

    def get_context_data(self, **kwargs):
        context = super(SendingCreate, self).get_context_data(**kwargs)
        context.update(sending_food_form=SendingForm())
        # board = Board.objects.all().order_by('id')
        # context.update({'boards': board})
        return context
