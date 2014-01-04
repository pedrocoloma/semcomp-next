# coding: utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.tests.utils import skipIfCustomUser
from django.core.urlresolvers import reverse
from django.template import Template, Context, RequestContext
from django.test import TestCase

class WebsiteTemplateTagsTests(TestCase):
	def setUp(self):
		self.anon_user = AnonymousUser()
		self.default_user = User.objects.create_user(
			'user',
			'email@provider.com',
			'pass',
			first_name='John',
			last_name='Doe',
		)
	
	def test_user_bar_content_no_user(self):
		out = Template(
			"{% load semcomp %}"
			"{% render_user_bar %}"
		).render(Context({
			'user': self.anon_user
		}))
		self.assertEqual(out.strip(), "")

	@skipIfCustomUser
	def test_user_bar_content_default_user(self):
		out = Template(
			"{% load semcomp %}"
			"{% render_user_bar %}"
		).render(Context({
			'user': self.default_user
		}))
		self.assertEqual(reverse('logout') in out, True)
		self.assertEqual('John Doe' in out, True)