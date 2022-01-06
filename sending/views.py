from sending.models import Sending
from sending.forms import SendingForm

from vanilla import model_views as views



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
