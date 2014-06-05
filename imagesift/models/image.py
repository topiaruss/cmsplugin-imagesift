from django.db import models
from django.utils.translation import ugettext_lazy as _

from imagestore.models.bases.image import BaseImage


class Image(BaseImage):
    """
    An image for the gallery, with special front-end behaviour when the video URL is populated.

    """
    class Meta(BaseImage.Meta):
        abstract = False
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        app_label = 'imagesift'

    album = models.ForeignKey('imagesift.Album', verbose_name=_('Album'), null=True, blank=True, related_name='images')

    video_url = models.URLField(_('Video URL'), default='')

    def has_video(self):
        """
        Use this for the logical testing of whether a video is present.
        """
        return self.video_url

