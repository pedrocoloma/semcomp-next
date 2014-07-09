from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import MultiColumns, Column

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

plugin_pool.register_plugin(MultiColumnsPlugin)
plugin_pool.register_plugin(ColumnPlugin)
plugin_pool.register_plugin(SchedulePlugin)
