from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import GalleryPlugin


class ImagesiftPlugin(CMSPluginBase):
    model = GalleryPlugin
    name = _('Imagesift Plugin')
    render_template = "imagesift_plugin.html"

    def date_digest(self, images):
        """
        return a list of unique dates, for all the images passed
        """
        dates = {}
        for i in images:
            dates.setdefault(i.overrideable_date().date(), None)
        return sorted(dates.keys())

    def render(self, context, instance, placeholder):
        url = context['request'].get_full_path()
        limit = instance.thumbnail_limit
        qs = instance.get_images_queryset()
        if limit:
            qs = qs[:limit]

        context.update({
            'dates': [d.isoformat() for d in self.date_digest(qs)],
            'images': qs,
            'instance': instance,
            'placeholder': placeholder,
            'url':url,
        })
        return context


plugin_pool.register_plugin(ImagesiftPlugin)