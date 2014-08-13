# coding: utf-8

import random
import string

from django import db
from django.conf import settings
from django.db import models

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
		except:
			pass
		# ...um id da base de dados...
		try:
			return SemcompUser.objects.get(id=badge), False
		except:
			pass
		# ...ou pode ser um mané que não fez inscrição na semcomp e devia
		# passar vergonha mas vou criar um usuário pra ele com o que deveria
		# ser o número usp. se não for, quero que ele se foda
		while True:
			try:
				domain = 'usuario-sem-cadastro.semcomp.icmc.usp.br'
				box = ''.join(random.sample(string.ascii_letters.lower(), 20))
				email = '{}@{}'.format(box, domain)
				user = SemcompUser.objects.create(id_usp=badge, email=email)
				return user, True
			except db.IntegrityError:
				# Se isso aconteceu é porque o email não é único, por incrível
				# que pareça. É bem pouco provável que o email rand ali de cima
				# seja escolhido duas vezes, mas se escolher, só faz de novo
				pass


class Attendance(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	event = models.ForeignKey('website.Event')

	objects = AttendanceManager()
