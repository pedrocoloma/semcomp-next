# coding: utf-8

from __future__ import unicode_literals

import logging

from django.test import TestCase
from django.test.utils import override_settings

from stats import add_event

from .config import StatsHandler

class StatsTest(TestCase):
	def setUp(self):
		self.handler = StatsHandler()

		logger = logging.getLogger('stats')
		logger.handlers = []
		logger.addHandler(self.handler)

	def assertEventCreated(self, group_type):
		def has_group(group):
			return lambda record: record.msg.get('@group') == group
		self.assertTrue(any(map(has_group(group_type), self.handler.records)))

class BasicStatsTest(StatsTest):
	def test_event_created(self):
		add_event('special-group-type', {'nonsense': 'data'})
		self.assertEventCreated('special-group-type')

