import datetime
import logging

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import GalleryPlugin
from .views import get_batch_context

logger = logging.getLogger(__name__)

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

    def photographer_digest(self, images):
        """
        return a list of unique photogs, for all the images passed
        """
        photogs = {}
        for i in images:
            photogs.setdefault(i.overrideable_photographer(), None)
        for trash in ['', None, u'']:
            photogs.pop(trash, None)
        return sorted(photogs.keys())

    def camera_model_digest(self, images):
        """
        return a list of unique cam models, for all the images passed
        """
        cams = {}
        for i in images:
            try:
                mod = i.exif_by_block()['Image']['Model']
                cams[mod] = None
            except KeyError:
                continue
        for trash in ['', None, u'']:
            cams.pop(trash, None)
        return sorted(cams.keys())

    def event_digest(self, images):
        """
        return a list of unique cam models, for all the images passed
        """
        events = {}
        for i in images:
            events.setdefault(i.event_name, None)
        for trash in ['', None, u'']:
            events.pop(trash, None)
        return sorted(events.keys())

    def render(self, context, instance, placeholder):
        url = context['request'].get_full_path()

        batch_data = get_batch_context(context['request'], instance, {})
        context.update(batch_data)
        context.update({
            'dates': [d.isoformat() for d in self.date_digest(batch_data['images'])],
            'events': self.event_digest(batch_data['images']),
            'models': self.camera_model_digest(batch_data['images']),
            'photogs': self.photographer_digest(batch_data['images']),
            'instance': instance,
            'placeholder': placeholder,
            'url':url,
        })

        # print context['dates']
        # print context['events']
        # print context['models']
        # print context['photogs']
        # print 'da', context['filtered_date']
        # print 'mo', context['filtered_model']
        # print 'ph', context['filtered_photog']
        # print 'ev', context['filtered_event']
        # print 'rev', context['reverse']

        return context


plugin_pool.register_plugin(ImagesiftPlugin)