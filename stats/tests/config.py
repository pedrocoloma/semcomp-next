import logging

class StatsHandler(logging.Handler):
	def __init__(self, *args, **kwargs):
		super(StatsHandler, self).__init__(*args, **kwargs)
		self.records = []
	def emit(self, record):
		self.records.append(record)
