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
    cache = False       # Important because we change response depending on the request, not just the instance.

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
            mod = i.safe_exif_by_block('Image', 'Model')
            cams[mod] = None
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

        DEBUGGING_THIS = 1

        if DEBUGGING_THIS:
            logger.info('PATH_INFO     : %s' % context['request'].META['PATH_INFO'])
            logger.info('QUERY_STRING  : %s' % context['request'].META['QUERY_STRING'])
            logger.info('dig dates     : %s' % context['dates'])
            logger.info('dig events    : %s' % context['events'])
            logger.info('dig models    : %s' % context['models'])
            logger.info('dig photogs   : %s' % context['photogs'])
            logger.info('filtered date : %s' % context['filtered_date'])
            logger.info('filtered modl : %s' % context['filtered_model'])
            logger.info('filtered phot : %s' % context['filtered_photog'])
            logger.info('filtered even : %s' % context['filtered_event'])
            logger.info('reverse       : %s' % context['reverse'])
            logger.info('result images : %s' % batch_data['images'])

        return context


plugin_pool.register_plugin(ImagesiftPlugin)