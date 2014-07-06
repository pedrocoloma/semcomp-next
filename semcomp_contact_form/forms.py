from django import forms
from contact_form.forms import ContactForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import loader

class SemcompContactForm(ContactForm):
    """

    Other notes for subclassing
    ---------------------------

    Subclasses which want to inspect the current ``HttpRequest`` to
    add functionality can access it via the attribute ``request``; the
    base ``message`` takes advantage of this to use ``RequestContext``
    when rendering its template. See the ``AkismetContactForm``
    subclass in this file for an example of using the request to
    perform additional validation.

    Subclasses which override ``__init__`` need to accept ``*args``
    and ``**kwargs``, and pass them via ``super`` in order to ensure
    proper behavior.

    Subclasses should be careful if overriding ``_get_message_dict``,
    since that method **must** return a dictionary suitable for
    passing directly to ``send_mail`` (unless ``save`` is overridden
    as well).

    Overriding ``save`` is relatively safe, though remember that code
    which uses your form will expect ``save`` to accept the
    ``fail_silently`` keyword argument. In the base implementation,
    that argument defaults to ``False``, on the assumption that it's
    far better to notice errors than to silently not send mail from
    the contact form.
    
    """

    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'Nome','required':'true'}))
    email = forms.EmailField(max_length=200,
                             widget=forms.EmailInput(attrs={'placeholder': 'E-mail','required':'true'}),
                           required = True)
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Mensagem...','required':'true'}),
                           required = True)
    
    #from_email = settings.DEFAULT_FROM_EMAIL
    
    #recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

    subject_template_name = "contact_form/contact_form_subject.txt"
    
    template_name = 'contact_form/contact_form_message.txt'


    # enviar e-mail para os administradores e para a pessoa que enviou o e-mail
    # o e-mail enviado para a pessoa que entrou em contato informara apenas que o e-mail foi recebido.
    def save(self, fail_silently=False):
        data = self.get_message_dict()
        msg = EmailMultiAlternatives(subject=data['subject'], body=data['message'], from_email=data['from_email'], to=data['recipient_list'])

        msg.attach_alternative(loader.render_to_string('contact_form/contact_form_message.html', self.get_context()), "text/html")
        msg.send(fail_silently=fail_silently)

        data = {}
        data['subject'] = 'Contato Semcomp'
        data['message'] = loader.render_to_string('contact_form/contact_form_message_sender.txt', self.get_context())
        data['from_email'] = self.from_email
        data['recipient_list'] = [self.cleaned_data['email']]

        msg = EmailMultiAlternatives(subject=data['subject'], body=data['message'], from_email=data['from_email'], to=data['recipient_list'])

        msg.attach_alternative(loader.render_to_string('contact_form/contact_form_message_sender.html', self.get_context()), "text/html")
        msg.send(fail_silently=fail_silently)

        #send_mail(fail_silently=fail_silently, **self.get_message_dict())