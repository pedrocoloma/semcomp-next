from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import Column

class ColumnsPlugin(CMSPluginBase):
	model = CMSPlugin
	name = _(u'Columns')
	render_template = 'website/plugins/columns_plugin.html'
	allow_children = True
	child_classes = ['ColumnPlugin']

class ColumnPlugin(CMSPluginBase):
	model = Column
	name = _('Column')
	render_template = 'website/plugins/single_column_plugin.html'
	allow_children = True

plugin_pool.register_plugin(ColumnsPlugin)
plugin_pool.register_plugin(ColumnPlugin)
