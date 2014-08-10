# coding: utf-8

from datetime import datetime, timedelta
import json

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import utc, now
from django.views.decorators.http import require_http_methods

import bleach

import stats
from semcomp_contact_form.models import Message
from website.models import SemcompUser

from ..forms import MessageForm, NewMessageForm
from ..decorators import staff_required

def render_json_response(data, **kwargs):
	return HttpResponse(
		json.dumps(data),
		content_type='application/json',
		**kwargs
	)

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
			# é, isso é um pouco estranho, mas 1) o admin pode mudar de
			# nome/email e eu quero guardar os dados de como que foi a mensagem
			# 2) o mesmo modelo é usado pra mensagens do form e mensagens aqui,
			# então precisa dos dois
			# 3) estou considerando que "precisa" é um "precisa", apesar de não
			# ser algo tão importante...
			new_message.from_name = request.user.full_name
			new_message.from_email = request.user.email
			new_message.sent_by = request.user
			# isso é só uma resposta
			new_message.is_announcement = False

			new_message.save()

			new_message.send_as_reply()

			# o last_ping vai lá pra trás pra não aparecer como sendo respondida
			message.last_ping = datetime(2000, 1, 1).replace(tzinfo=utc)
			message.save()

			stats.add_event(
				'management-messages',
				{
					'action': 'reply',
					'to_message': {
						'id': message.id,
						'from_email': message.from_email,
						'from_name': message.from_name,
					},
					'user': {
						'id': request.user.pk,
						'name': request.user.full_name,
					}
				}
			)

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

	stats.add_event(
		'management-messages',
		{
			'action': 'delete',
			'message_list': [
				{
					'id': m.pk,
					'from_name': m.from_name,
					'from_email': m.from_email,
				} for m in list(message.replies.all()) + [message]
			],
			'user': {
				'id': request.user.pk,
				'name': request.user.full_name
			}
		}
	)

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
			to_type = form.cleaned_data['type']
			to_user = form.cleaned_data['to_email']
			if to_type == 'one':
				users = [form.cleaned_data['to_email']]
			elif to_type == 'bulk':
				users = SemcompUser.objects.registered()
			elif to_type == 'no_payment':
				users = SemcompUser.objects.no_payment()
			elif to_type == 'pending':
				users = SemcompUser.objects.pending()
			elif to_type == 'paid':
				users = SemcompUser.objects.paid()
			elif to_type == 'coffee':
				users = SemcompUser.objects.coffee()
			elif to_type == 'no_coffee':
				users = SemcompUser.objects.no_coffee()
			
			stats_data = {
				'action': 'send',
				'user': {
					'id': request.user.pk,
					'name': request.user.full_name,
				},
				'message': {
					'type': to_type,
					'subject': form.cleaned_data['subject'],
				}
			}
			if to_type == 'one':
				stats_data['message']['recipient'] = to_user.email
			stats.add_event('management-messages', stats_data)

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

@staff_required
@require_http_methods(['GET', 'POST'])
def messages_ping(request):
	response = {}
	if request.method == 'GET':
		ids = request.GET.getlist('ids[]')
		remove_self = 'removeSelf' in request.GET

		try:
			ids = map(int, ids)
			
			messages = Message.objects.filter(pk__in=ids)
			name = lambda u: u.full_name if u else None

			response['data'] = {}
			for m in messages:
				if remove_self:
					if m.last_ping_by == request.user:
						continue
				response['data'][m.pk] = [
					m.is_being_replied_to(),
					name(m.last_ping_by)
				]
		except ValueError:
			response['error'] = u'IDs inválidos'
	else:
		ids = request.POST.getlist('ids[]')
		try:
			ids = map(int, ids)

			messages = Message.objects.filter(pk__in=ids)
			for m in messages:
				# não altera quem tá mexendo numa mensagem se outro
				# apressadinho quiser responder em cima
				if m.is_being_replied_to() and m.last_ping_by != request.user:
					continue
				m.last_ping = now()
				m.last_ping_by = request.user
				m.save()
		except ValueError:
			response['error'] = u'IDs inválidos'

	return render_json_response(response)
