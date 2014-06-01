# -*- coding: utf-8 -*-

from django.db import models

from cms.models.pluginmodel import CMSPlugin
from imagestore.models import Image
from tagging.models import TaggedItem


class GalleryPlugin(CMSPlugin):
    filter = models.TextField()
    thumbnail_geometry = models.CharField(max_length=50)
    image_geometry = models.CharField(max_length=50)
    thumbnail_limit = models.IntegerField(default=0)  # 0 means no limit

    def get_images_queryset(self):
        return TaggedItem.objects.get_by_model(Image, [self.filter])

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