# coding: utf-8

from __future__ import unicode_literals

from StringIO import StringIO

from django.contrib.auth import get_user_model
from django.test.client import Client

from PIL import Image

from stats.tests import StatsTest

class ManagementTest(StatsTest):
	def setUp(self):
		super(ManagementTest, self).setUp()

		UserModel = get_user_model()
		self.user = UserModel.objects.create_superuser(
			'test@user.com',
			'Usuário Teste',
			'12345678',
			'senha',
		)

		self.client = Client()
		self.client.login(email=self.user.email, password='senha')

	def get_blank_image(self):
		# imagem branca de 64x64 pixels
		im = Image.new('RGB', (64, 64), (255, 255, 255))
		output = StringIO()
		im.save(output, format='PNG')
		output.seek(0)
		return output
