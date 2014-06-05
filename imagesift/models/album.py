from django.utils.translation import ugettext_lazy as _
from django.db import models

from imagestore.models.bases.album import BaseAlbum


class Album(BaseAlbum):

    class Meta(BaseAlbum.Meta):
        abstract = False
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        app_label = 'imagesift'

    head = models.ForeignKey('imagesift.Image', related_name='head_of', null=True, blank=True, on_delete=models.SET_NULL)
