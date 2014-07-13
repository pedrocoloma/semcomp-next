from django.utils.translation import ugettext as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import MinicursosPluginModel
from website.models import Course
class MinicursosPlugin(CMSPluginBase):
	model = MinicursosPluginModel
	name = _(u'Minicursos')
	render_template = "minicursos/render_minicursos.html"

	def render(self, context, instance, placeholder):
		context.update({
			'instance': instance,
			'courses': Course.objects.order_by('title')
			})
		return context

plugin_pool.register_plugin(MinicursosPlugin)
