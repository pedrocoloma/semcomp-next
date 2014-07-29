# coding: utf-8

from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone

from website.models import SemcompUser


class MessageManager(models.Manager):
	def unanswered(self):
		return self.filter(
			being_replied=False,
			in_reply_to=False,
		)

class Message(models.Model):
	last_ping = models.DateTimeField(
		# o valor padrão é bem antigo pra que o is_being_replied não
		# apite quando a mensagem acabou de ser criada
		default=datetime(2000, 1, 1).replace(tzinfo=timezone.utc)
	)
	in_reply_to = models.ForeignKey(
		'self',
		null=True,
		related_name='replies'
	)
	sent_by = models.ForeignKey(
		SemcompUser,
		null=True,
		on_delete=models.SET_NULL,
		related_name='replied_messages'
	)

	from_name = models.CharField(max_length=100)
	from_email = models.EmailField(max_length=254)
	body = models.TextField()
	html_body = models.TextField()
	date_sent = models.DateTimeField(auto_now_add=True)

	objects = MessageManager()

	def replied(self):
		return self.replies.count() > 0

	def is_old(self):
		current_day = timezone.localtime(timezone.now()).date().day
		sent_day = timezone.localtime(self.date_sent).date().day
		return current_day != sent_day

	def is_being_replied_to(self):
		dt = timezone.now() - self.last_ping
		# mais que 100 segundos parado é motivo de treta
		if dt.days == 0 and dt.seconds <= 100:
			return True
		else:
			return False
	
	def send_as_reply(self):
		if not self.pk:
			return
		if not self.in_reply_to:
			raise ValueError(_(u'Mensagem não é uma resposta'))

		msg = EmailMultiAlternatives(
			_(u'Contato Semcomp 17'),
			self.body,
			self.from_email,
			[self.in_reply_to.from_email]
		)
		msg.attach_alternative(self.html_body, 'text/html')
		msg.send()
