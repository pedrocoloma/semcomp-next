# coding: utf-8

from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import utc

import bleach

from semcomp_contact_form.models import Message

from ..forms import MessageForm
from ..decorators import staff_required

@staff_required
def manage_messages(request):
	context = {
		'active_messages': True,
		# o nome disso aqui foi escolhido como email_messages ao invés de
		# messages por causa disso aqui:
		# https://docs.djangoproject.com/en/dev/ref/contrib/messages/
		'email_messages': Message.objects.filter(in_reply_to=None).order_by('-date_sent')
	}

	return render(request, 'management/messages.html', context)

@staff_required
def messages_detail(request, message_pk):
	message = get_object_or_404(Message, pk=message_pk)
	form = MessageForm(request.POST or None)

	if request.method == 'POST':
		if form.has_changed() and form.is_valid():
			new_message = form.save(commit=False)
			new_message.body = bleach.clean(
				new_message.html_body, strip=True, tags=['a'])
			new_message.in_reply_to = message
			# o last_ping vai lá pra trás de novo pra não ter treta
			new_message.last_ping = datetime(2000, 1, 1).replace(tzinfo=utc)
			# é, isso é um pouco estranho, mas 1) o admin pode mudar de
			# nome/email e eu quero guardar os dados de como que foi a mensagem
			# 2) o mesmo modelo é usado pra mensagens do form e mensagens aqui,
			# então precisa dos dois
			# 3) estou considerando que "precisa" é um "precisa", apesar de não
			# ser algo tão importante...
			new_message.from_name = request.user.full_name
			new_message.from_email = request.user.email
			new_message.sent_by = request.user

			new_message.save()

			new_message.send_as_reply()

			return redirect('management_messages')


	context = {
		'active_messages': True,
		'email_message': message,
		'replies': message.replies.all(),
		'form': form
	}
	return render(request, 'management/messages_detail.html', context)
