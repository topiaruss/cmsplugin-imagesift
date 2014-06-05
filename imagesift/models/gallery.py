# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from imagesift.models import Image
from tagging.models import TaggedItem



class GalleryPlugin(CMSPlugin):
    class Meta(object):
        abstract = False
        app_label = 'imagesift'

    thumbnail_geometry = models.CharField(max_length=50, default='50x50',
                                          help_text=_('Examples: "50x30", "50", "x30"'))
    thumbnail_limit = models.IntegerField(default=0,
                                          help_text=_('Maximum count of items to show. 0 means no limit.'))
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
        # temporarily order by the date added to the imagestore, later by exif image date?
        images = images.order_by('created')
        return images

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

# Override for imagestore Image model

