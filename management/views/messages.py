# coding: utf-8

from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import utc

import bleach

from semcomp_contact_form.models import Message
from website.models import SemcompUser

from ..forms import MessageForm, NewMessageForm
from ..decorators import staff_required

@staff_required
def manage_messages(request):
	context = {
		'active_messages': True,
		# o nome disso aqui foi escolhido como email_messages ao invés de
		# messages por causa disso aqui:
		# https://docs.djangoproject.com/en/dev/ref/contrib/messages/
		'email_messages': Message.objects \
			.filter(is_announcement=False, in_reply_to=None) \
			.order_by('-date_sent'),
		'announcements': Message.objects.announcements().order_by('-date_sent'),
	}

	return render(request, 'management/messages.html', context)

@staff_required
def messages_detail(request, message_pk):
	message = get_object_or_404(Message, pk=message_pk)
	form = MessageForm(request.POST or None)

	if request.method == 'POST' and not message.is_announcement:
		if form.has_changed() and form.is_valid():
			new_message = form.save(commit=False)
			new_message.body = bleach.clean(
				new_message.html_body, strip=True, tags=['a'])
			new_message.in_reply_to = message
			new_message.to_email = message.from_email
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

@staff_required
def messages_delete(request, message_pk):
	message = get_object_or_404(Message, pk=message_pk)

	# delete cascade nas respostas
	message.delete()

	return redirect('management_messages')

@staff_required
def messages_new(request):
	form = NewMessageForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			text_body = bleach.clean(
				form.cleaned_data['body'],
				strip=True,
				tags=['a'],
			)

			# salva mensagem pra registro
			msg = Message.objects.create(
				# abusa o campo "body" pra colocar o assunto
				body=form.cleaned_data['subject'],
				to_email=getattr(form.cleaned_data['to_email'], 'email', ''),
				# o html_body é o conteúdo real da mensagem
				html_body=form.cleaned_data['body'],
				# dados da pessoa que mandou, pra poder apontar dedos depois
				sent_by=request.user,
				from_name=request.user.full_name,
				from_email=request.user.email,
				# marca que é uma divulgação
				is_announcement=True,
			)


			# determina pra quem vai a mensagem
			if form.cleaned_data['type'] == 'one':
				users = [form.cleaned_data['to_email']]
			else:
				users = SemcompUser.objects.registered()

			for user in users:
				msg = EmailMultiAlternatives(
					form.cleaned_data['subject'],
					text_body,
					settings.DEFAULT_FROM_EMAIL,
					to=[user.email],
				)
				msg.attach_alternative(form.cleaned_data['body'], 'text/html')
				msg.send()

			return redirect('management_messages')

	context = {
		'active_messages': True,
		'form': form
	}
	return render(request, 'management/messages_new.html', context)
