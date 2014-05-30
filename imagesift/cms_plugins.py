from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import GalleryPlugin


class ImagesiftPlugin(CMSPluginBase):
    model = GalleryPlugin
    name = _('Imagesift Plugin')
    render_template = "imagesift_plugin.html"

    def render(self, context, instance, placeholder):
        url = context['request'].get_full_path()
        context.update({
            'images':instance.get_images_queryset(),
            'instance':instance,
            'placeholder':placeholder,
            'url':url,
        })
        return context


plugin_pool.register_plugin(ImagesiftPlugin)