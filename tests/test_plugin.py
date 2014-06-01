#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cms.test_utils.testcases import CMSTestCase
from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.test.utils import override_settings

from django.test.client import Client
from django.core.urlresolvers import reverse
from imagestore.models import *
from lxml import html
from tagging.models import Tag, TaggedItem
from tagging.fields import TagField
from imagesift.cms_plugins import ImagesiftPlugin, GalleryPlugin
import os


class ImagesiftPluginFilterTest(TestCase):

    def setUp(self):
        self.image_file = open(os.path.join(os.path.dirname(__file__), 'test_img.jpg'))
        self.album = Album(name='test album')
        self.album.save()
        details = (
            ('i1', 'alpha            rho'),
            ('i2', '      beta       rho'),
            ('i3', '           gamma rho'),
        )
        self.image_count = len(details)
        for title, tags in details:
            Image(title=title, image=File(self.image_file), tags=tags).save()
        self.image1 = Image.objects.get(title__exact='i1')

    def test_single_filter(self):
        gall_row = GalleryPlugin(filter='alpha')
        gall_row.save()
        gall = ImagesiftPlugin()
        ret = gall.render({}, gall_row, 'xxx')
        self.assertEqual(len(ret['images']), 1)

    def test_multi_filter(self):
        gall_row = GalleryPlugin(filter='rho')
        gall_row.save()
        gall = ImagesiftPlugin()
        ret = gall.render({}, gall_row, 'xxx')
        self.assertEqual(len(ret['images']), self.image_count)


class ImagesiftRenderTest(TestCase):

    def setUp(self):
        self.plugin = ImagesiftPlugin()

        self.image_file = open(os.path.join(os.path.dirname(__file__), 'test_img.jpg'))
        details = (
            ('i1', 'alpha            rho'),
            ('i2', '      beta       rho'),
            ('i3', '           gamma rho'),
        )
        self.image_count = len(details)
        for title, tags in details:
            Image(title=title, image=File(self.image_file), tags=tags).save()

    def test_plugin(self):
        # I'd love this to test rendered html, but see
        #   https://github.com/divio/django-cms/issues/3214
        context = {}
        instance = GalleryPlugin(filter='alpha')
        instance.save()
        out_context = self.plugin.render(context, instance, None)
        self.assertEqual('i1', out_context['images'][0].title)

@override_settings(ROOT_URLCONF='imagesift.tests.test_urls')
class ImagesiftTests(CMSTestCase):

    def test_gallery_page(self):
        pass
        #test_url = reverse('myapp_view_name')
        # rest of test as normal
