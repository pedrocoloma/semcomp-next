# coding: utf-8

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

class CourseRegistration(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	course = models.ForeignKey('website.Course')

	class Meta:
		unique_together = ('user', 'course')

	class PagamentoNaoRealizado(Exception):
		def __init__(self):
			self.msg = u'Usuário não pode realizar a inscrição: Pagamento não realizado'
	class PacotesDiferentes(Exception):
		def __init__(self, minicurso):
			self.msg = u'Não é possível realizar a inscrição em minicursos de pacotes diferentes. Conflito: %s' % minicurso
	class VagasEsgotadas(Exception):
		def __init__(self):
			self.msg = u'As vagas neste minicurso estão esgotadas'
	class ConflitoDeHorario(Exception):
		def __init__(self, minicurso):
			self.minicurso = minicurso
			self.msg= u'Já inscrito em um minicurso no mesmo dia: %s' % minicurso


def get_user_courses(user):
	user_courses = CourseRegistration.objects.filter(user=user)

	for reg in user_courses:
		course = reg.course
		course.annotate_times()

	return user_courses

@receiver(pre_save, sender=CourseRegistration)
def regras_minicurso(sender, instance, **kwargs):
	try:
		from website import models as website_models
		inscricao = website_models.Inscricao.objects.get(user=instance.user)
		if not inscricao.pagamento:
			raise
	except:
		raise CourseRegistration.PagamentoNaoRealizado()
	instance.course.annotate_times()
	user_courses = get_user_courses(instance.user)
	for user_course in user_courses:
		if user_course.course.id == instance.course.id:
			return # se for novo registro vai dar IntegrityError mais pra frente...
		if user_course.course.start_date == instance.course.start_date:
			raise CourseRegistration.ConflitoDeHorario(user_course.course.title)
		if user_course.course.track != instance.course.track:
			raise CourseRegistration.PacotesDiferentes(user_course.course.title)

	if instance.course.get_remaining_vacancies() == 0:
		raise CourseRegistration.VagasEsgotadas()
