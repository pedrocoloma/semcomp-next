# coding: utf-8

import logging

from django.utils.timezone import now

def add_event(group, data):
	logger = logging.getLogger(__name__)

	if '@group' in data:
		raise ValueError(u'@group em evento')
	if '@timestamp' in data:
		raise ValueError(u'@timestamp em evento')
	if not isinstance(data, dict):
		raise TypeError(u'data deve ser um dicionário')

	record = {
		'@group': group,
		'@timestamp': now().isoformat(),
	}
	record.update(data)

	logger.debug(record)

