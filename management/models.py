# coding: utf-8

import random
import string

from django import db
from django.conf import settings
from django.db import models

import stats

from website.models import SemcompUser


class AttendanceManager(models.Manager):
	def get_or_create_from_badge(self, event, badge_number):
		badge = badge_number.strip().lstrip('0')
		user,created = self.__get_user_from_badge(badge)

		return Attendance.objects.get_or_create(user=user, event=event)

	def __get_user_from_badge(self, badge):
		# O crachá pode ser um número usp...
		try:
			return SemcompUser.objects.get(id_usp=badge), False
		except SemcompUser.MultipleObjectsReturned:
			# isso é falha na especificação do modelo de usuário: o número USP
			# deveria ser único mas não é. Pega o primeiro da lista (ordenada,
			# pra ser consistente) e usa pra presença
			users = SemcompUser.objects.filter(id_usp=badge).order_by('id')

			stats_data = {
				'action': 'duplicate',
				'badge': badge,
				'users': [],
			}
			for u in users:
				stats_data['users'].append({
					'id': u.id,
					'full_name': u.full_name,
					'id_usp': u.id_usp,
				})
			stats.add_event('management-attendance', stats_data)

			return users[0], False
		except:
			pass
		# ...um id da base de dados...
		try:
			# nesse caso, precisa tirar o "1" da frente e os zeros
			# que sobraram porque algum imbecil achou que alterar
			# os dados que você tem "porque sim" é uma ótima ideia
			#
			# consequência: não tirar '1' se o número é pequeno, porque pode
			# ser algo do tipo "133" que é um id digitado na mão
			if len(badge_id) > 4:
				badge_id = badge.lstrip('1').lstrip('0')
			else:
				badge_id = badge.lstrip('0')
			return SemcompUser.objects.get(id=badge_id), False
		except:
			pass
		# ...ou pode ser um mané que não fez inscrição na semcomp e devia
		# passar vergonha mas vou criar um usuário pra ele com o que deveria
		# ser o número usp. se não for, quero que ele se foda
		try:
			# cria o usuário usando o nusp como email. isso ajuda a
			# garantir unicidade dos cadastros automaticamente
			domain = 'usuario-sem-cadastro.semcomp.icmc.usp.br'
			email = '{}@{}'.format(badge, domain)
			user = SemcompUser.objects.create(id_usp=badge, email=email)
			return user, True
		except db.IntegrityError:
			# se isso acontecer, algo muito ruim deu errado. registra a ação e
			# joga um erro porque isso é sério
			stats.add_event(
				'management-attendance',
				{
					'action': 'error',
					'badge': badge,
					'event': {
						'id': event.pk,
						'name': event.name(),
					}
				}
			)
			raise


class Attendance(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	event = models.ForeignKey('website.Event')

	objects = AttendanceManager()
