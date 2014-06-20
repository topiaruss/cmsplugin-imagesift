# -*- coding: utf-8 -*-
import datetime
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from imagestore.models import Image
from tagging.models import TaggedItem

logger = logging.getLogger(__name__)


class GalleryPlugin(CMSPlugin):
    class Meta(object):
        abstract = False
        app_label = 'imagesift'

    thumbnail_geometry = models.CharField(max_length=50, default='50x50',
                                          help_text=_('Examples: "50x30", "50", "x30"'))
    thumbnail_limit = models.IntegerField(default=0,
                                          help_text=_('Maximum count of items in a batch. 0 means no limit.'))
    image_geometry = models.CharField(max_length=50, default='300x200',
                                      help_text=_('Examples: "600x400", "600", "x400"'))
    filter = models.TextField(help_text=_('Items matching ALL these tags will be shown. One tag per line.'))

    def get_images_queryset(self):
        """
        The universal queryset generator for the plugin
        """
        tags = self.filter.splitlines()
        tags = [t.strip() for t in tags]
        images = TaggedItem.objects.get_by_model(Image, tags)
        return images

    def sort_by_overrideable_date(self, qs):
        try:
            qs.sort(key=lambda i: i.overrideable_date())
        except TypeError:
            # poss "can't compare offset-naive and offset-aware datetimes"
            logger.exception('comparison of naiive/smart dates?')
            for i in qs:
                logger.debug('overridable_date : %s' % i.overrideable_date().isoformat())
        return qs

    def get_immediate_neighbours(self, image):
        """
         Return tuple of prev and next images in the list. Bear in mind that the list is computed on the fly,
         so may change as the user is navigating
        """
        # create forward and reverse maps
        images = self.get_images_queryset()
        immap = dict(enumerate(map(lambda x: x['id'], images.values('id'))))  # e.g. {0: 3, 1: 14}
        rev_immap = dict((v,k) for k,v in immap.items())

        # work out the ids of the prev and next items in the result set
        pos = rev_immap[image.id]
        prev = pos-1 if pos else  None
        next = pos+1 if pos < len(immap)-1 else None
        if prev is not None:
            prev = images.get(id__exact=immap[prev])
        if next is not None:
            next = images.get(id__exact=immap[next])
        return prev, next

    def get_filtered_queryset_bundle(self, request):
        """
        this is called from a view, and uses request variables to filter the return set, returning
        the salient variables. This means that we should be able to get away with adding filters just by
        changing this, and its template.
        """
        url = request.get_full_path()
        qs = self.get_images_queryset()

        # there's no way to avoid listing, sorry -- we need to filter on a computed value.
        # OPTIMISE: overrideable date could be replace at the query level with a few hours' work.  Not worth it.
        qs = list(qs)

        date = request.GET.get('date')
        filtered_date = None
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            qs = [i for i in qs if i.overrideable_date().date() == date]
            filtered_date = unicode(date)

        event = request.GET.get('event')
        filtered_event = None
        if event:
            qs = [i for i in qs if i.event_name == event]
            filtered_event = event

        model = request.GET.get('model')
        filtered_model = None
        if model:
            qs = [i for i in qs if i.exif_by_block()['Image']['Model'] == model]
            filtered_model = model

        photog = request.GET.get('photog')
        filtered_photog = None
        if photog:
            qs = [i for i in qs if i.overrideable_photographer() == photog]
            filtered_photog = photog

        # sort before reverse
        qs = self.sort_by_overrideable_date(qs)

        # reverse after sort
        reverse = request.GET.get('reverse')
        if reverse:
            qs.reverse()

        ret = dict(
            images=qs,
            date=('' if date is None else date),
            event=('' if event is None else event),
            filtered_date=filtered_date,
            filtered_event=filtered_event,
            filtered_model=filtered_model,
            filtered_photog=filtered_photog,
            model=('' if model is None else model),
            photog=('' if photog is None else photog),
            reverse=('' if reverse is None else reverse) )
        print ret
        return ret