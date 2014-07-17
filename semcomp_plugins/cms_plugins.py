from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import MultiColumns, Column, MinicursosPluginModel
from website.models import Course

class MultiColumnsPlugin(CMSPluginBase):
	model = MultiColumns
	name = _(u'Multi columns')
	render_template = 'website/plugins/columns_plugin.html'
	allow_children = True
	child_classes = ['ColumnPlugin']

class ColumnPlugin(CMSPluginBase):
	model = Column
	name = _('Column')
	render_template = 'website/plugins/single_column_plugin.html'
	allow_children = True
	parent_classes = ['MultiColumnsPlugin']
	require_parent = True

class SchedulePlugin(CMSPluginBase):
	model = CMSPlugin
	render_template = 'semcomp_plugins/schedule_plugin.html'

class MinicursosPlugin(CMSPluginBase):
	model = MinicursosPluginModel
	name = _(u'Minicursos')
	render_template = "semcomp_plugins/render_minicursos.html"

	def render(self, context, instance, placeholder):
		context.update({
			'instance': instance,
			'courses': Course.objects.order_by('title')
			})
		return context

plugin_pool.register_plugin(MultiColumnsPlugin)
plugin_pool.register_plugin(ColumnPlugin)
plugin_pool.register_plugin(SchedulePlugin)
plugin_pool.register_plugin(MinicursosPlugin)