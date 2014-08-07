# coding: utf-8

from django.db import models
from django.conf import settings

from website.models import Course

class CourseRegistration(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	course = models.ForeignKey(Course)

	class Meta:
		unique_together = ('user', 'course')
