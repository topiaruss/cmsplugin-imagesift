from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

class ImagesiftPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _('Imagesift Plugin')
    render_template = "imagesift_plugin.html"

    def render(self, context, instance, placeholder):
        return dict(instance=instance, placeholder=placeholder)


plugin_pool.register_plugin(ImagesiftPlugin)