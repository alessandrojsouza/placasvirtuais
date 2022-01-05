from emails.models import Email
from emails.forms import EmailForm

from vanilla import model_views as views



class BaseEmailView(object):
    model = Email
    form_class = EmailForm
    lookup_field = 'pk'


class EmailList(BaseEmailView, views.ListView):
    template_name = 'emails/list.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(EmailList, self).get_context_data(**kwargs)
        context.update(subject=self.request.GET.get('subject', ''))
        return context

    def get_queryset(self):
        queryset = super(EmailList, self).get_queryset()
        queryset = queryset.all().order_by('id', 'subject')
        return queryset
