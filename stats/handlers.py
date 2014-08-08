import logging

from django.conf import settings

from stats.tasks import send_to_elasticsearch

class ElasticSearchHandler(logging.Handler):
	def emit(self, record):
		raw = record.msg

		send_to_elasticsearch.delay(settings.ELASTICSEARCH_INDEX, raw)

