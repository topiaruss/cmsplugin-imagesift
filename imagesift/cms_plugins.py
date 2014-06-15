import datetime
import logging

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import GalleryPlugin

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

    def sort_by_overrideable_date(self, qs):
        try:
            qs.sort(key=lambda i: i.overrideable_date())
        except TypeError:
            # poss "can't compare offset-naive and offset-aware datetimes"
            logger.exception('comparison of naiive/smart dates?')
            for i in qs:
                logger.debug('overridable_date : %s' % i.overrideable_date().isoformat())
        return qs


    def render(self, context, instance, placeholder):
        url = context['request'].get_full_path()
        date = context['request'].GET.get('date')
        limit = instance.thumbnail_limit
        qs = instance.get_images_queryset()
        # there's no way around listing, sorry.
        qs = list(qs)

        filtered = False
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            qs = [i for i in qs if i.overrideable_date().date() == date]
            filtered = _('The set of images is filtered to %s' % unicode(date))

        # sort before limit
        qs = self.sort_by_overrideable_date(qs)

        if limit:
            qs = qs[:limit]

        context.update({
            'dates': [d.isoformat() for d in self.date_digest(qs)],
            'filtered':filtered,
            'images': qs,
            'instance': instance,
            'placeholder': placeholder,
            'url':url,
        })
        return context


plugin_pool.register_plugin(ImagesiftPlugin)