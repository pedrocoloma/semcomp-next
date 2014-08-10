from django.conf import settings

from elasticsearch import Elasticsearch
from celery import shared_task

@shared_task
def send_to_elasticsearch(index, data):
	elasticsearch = Elasticsearch('elasticsearch')

	group = data.pop('@group', 'undefined-group-type')

	elasticsearch.index(index=index, doc_type=group, body=data)
