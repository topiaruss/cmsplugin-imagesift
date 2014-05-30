#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cms.test_utils.testcases import CMSTestCase
from django.core.files import File
from django.test.utils import override_settings
from imagestore.models import (Album, Image)
from cms.api import add_plugin
from cms.models import Placeholder

from imagesift.cms_plugins import ImagesiftPlugin
from imagesift.models import GalleryPlugin

class ImagesiftPluginFilterTest(CMSTestCase):

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
        ret = gall.render(self.get_context(path='/'), gall_row, 'xxx')
        self.assertEqual(len(ret['images']), 1)

    def test_multi_filter(self):
        gall_row = GalleryPlugin(filter='rho')
        gall_row.save()
        gall = ImagesiftPlugin()
        ret = gall.render(self.get_context(path='/'), gall_row, 'xxx')
        self.assertEqual(len(ret['images']), self.image_count)


class ImagesiftRenderTest(CMSTestCase):

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


    def test_plugin_context(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
          placeholder,
          ImagesiftPlugin,
          'en',
          filter='alpha'
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render(self.get_context(path='/'), model_instance, None)
        self.assertEqual('i1', context['images'][0].title)

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
          placeholder,
          ImagesiftPlugin,
          'en',
          filter='alpha'
         )
        html = model_instance.render_plugin(self.get_context(path='/'))
        self.assertIn('i1', html)


@override_settings(ROOT_URLCONF='imagesift.tests.test_urls')
class ImagesiftTests(CMSTestCase):

    def test_gallery_page(self):
        pass
        #test_url = reverse('myapp_view_name')
        # rest of test as normal
