# coding: utf-8

from django import forms
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template import RequestContext
from django.template import loader

from .models import Message

from contact_form.forms import ContactForm


class SemcompContactForm(ContactForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Nome','required':'true'}
        )
    )
    email = forms.EmailField(
        max_length=200,
        widget=forms.EmailInput(
            attrs={'placeholder': 'E-mail','required':'true'}
        ),
        required = True
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Mensagem...','required':'true'}
        ),
        required = True
    )
    
    subject_template_name = "contact_form/contact_form_subject.txt"
    template_name = 'contact_form/contact_form_message.txt'

    def get_context(self):
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(self.request)


        context = dict(
            self.cleaned_data,
            site=site
        )
        if hasattr(self, 'message_instance'):
            context.update({
                'message_instance': getattr(self, 'message_instance')
            })

        return RequestContext(self.request, context)

    # enviar e-mail para os administradores e para a pessoa que enviou o e-mail
    # o e-mail enviado para a pessoa que entrou em contato informara apenas que o e-mail foi recebido.
    def save(self, fail_silently=False):
        # Salva a mensagem no banco de dados pra poder responder por lá
        self.message_instance = Message.objects.create(
            from_name=self.cleaned_data['name'],
            from_email=self.cleaned_data['email'],
            body=self.cleaned_data['body'],
            is_announcement=False,
        )

        # Coloca o nono objeto no contexto pra poder usar em templates
        context = self.get_context()
        data = self.get_message_dict()

        # Avisa os admins que tem mensagem nova no pedaço
        msg = EmailMultiAlternatives(
            subject=data['subject'],
            body=data['message'],
            from_email=data['from_email'],
            to=data['recipient_list']
        )

        msg.attach_alternative(
            loader.render_to_string(
                'contact_form/contact_form_message.html',
                context
            ),
            "text/html"
        )
        msg.send(fail_silently=fail_silently)

        # Envia uma mensagem de confirmação pro usuário
        data = {}
        data['subject'] = u'Contato Semcomp 17'
        data['message'] = loader.render_to_string(
            'contact_form/contact_form_message_sender.txt',
            context
        )
        data['from_email'] = self.from_email
        data['recipient_list'] = [self.cleaned_data['email']]

        msg = EmailMultiAlternatives(
            subject=data['subject'],
            body=data['message'],
            from_email=data['from_email'],
            to=data['recipient_list']
        )

        msg.attach_alternative(
            loader.render_to_string(
                'contact_form/contact_form_message_sender.html',
                context
            ),
            "text/html"
        )
        msg.send(fail_silently=fail_silently)

