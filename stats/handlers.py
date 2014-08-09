import logging
import json

from django.conf import settings

from stats.tasks import send_to_elasticsearch

class ElasticSearchHandler(logging.Handler):
	def emit(self, record):
		raw = record.msg

		send_to_elasticsearch.delay(settings.ELASTICSEARCH_INDEX, raw)

class JSONFileHandler(logging.FileHandler):
	def emit(self, record):
		if isinstance(record.msg, dict):
			record.msg = json.dumps(record.msg, ensure_ascii=False)

		super(JSONFileHandler, self).emit(record)

