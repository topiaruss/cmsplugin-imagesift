# -*- coding: utf-8 -*-

from cms.models.pluginmodel import CMSPlugin
from django.db import models


class GalleryPlugin(CMSPlugin):
    filter = models.TextField()
