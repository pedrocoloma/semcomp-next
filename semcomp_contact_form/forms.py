from django import forms
from contact_form.forms import ContactForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import loader

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

    # enviar e-mail para os administradores e para a pessoa que enviou o e-mail
    # o e-mail enviado para a pessoa que entrou em contato informara apenas que o e-mail foi recebido.
    def save(self, fail_silently=False):
        data = self.get_message_dict()
        msg = EmailMultiAlternatives(
            subject=data['subject'],
            body=data['message'],
            from_email=data['from_email'],
            to=data['recipient_list']
        )

        msg.attach_alternative(
            loader.render_to_string(
                'contact_form/contact_form_message.html',
                self.get_context()
            ),
            "text/html"
        )
        msg.send(fail_silently=fail_silently)

        data = {}
        data['subject'] = 'Contato Semcomp'
        data['message'] = loader.render_to_string(
            'contact_form/contact_form_message_sender.txt',
            self.get_context()
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
                self.get_context()
            ),
            "text/html"
        )
        msg.send(fail_silently=fail_silently)

