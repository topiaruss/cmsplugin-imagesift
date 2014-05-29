from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import GalleryPlugin
from imagestore.models import Image
from tagging.models import TaggedItem


from django.utils.translation import ugettext_lazy as _

class ImagesiftPlugin(CMSPluginBase):
    model = GalleryPlugin
    name = _('Imagesift Plugin')
    render_template = "imagesift_plugin.html"

    def render(self, context, instance, placeholder):
        filter = instance.filter
        images = TaggedItem.objects.get_by_model(Image, [filter])
        context.update({
            'images':images,
            'object':instance,
            'placeholder':placeholder
        })
        return context


plugin_pool.register_plugin(ImagesiftPlugin)