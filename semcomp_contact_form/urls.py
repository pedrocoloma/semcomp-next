from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic import TemplateView

from contact_form.views import ContactFormView
from forms import SemcompContactForm


urlpatterns = patterns('',
                       url(r'^$',
                           ContactFormView.as_view(form_class=SemcompContactForm),
                           name='contact_form'),
                       url(r'^sent/$',
                           TemplateView.as_view(
                               template_name='contact_form/contact_form_sent.html'
                               ),
                           name='contact_form_sent'),
                       )
