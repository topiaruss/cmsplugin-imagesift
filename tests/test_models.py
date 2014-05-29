#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from imagestore.models import *
from lxml import html
from tagging.models import Tag, TaggedItem
from tagging.fields import TagField
import os


class ImagesiftTest(TestCase):

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

    def test_get_all_images(self):
        all = Image.objects.all()
        self.assertEqual(len(all), self.image_count)

    def test_smoketest_tagging_api(self):

        # get by model with string list
        all = TaggedItem.objects.get_by_model(Image, ['rho'])
        self.assertEqual(len(all), self.image_count)

        # get by model with string
        all = TaggedItem.objects.get_by_model(Image, 'rho')
        self.assertEqual(len(all), self.image_count)

        # get by model with tag Querysets
        all = TaggedItem.objects.get_union_by_model(Image, ['rho'])
        self.assertEqual(len(all), self.image_count)

        # add a tag
        all = Image.objects.all()
        for img in all:
            Tag.objects.add_tag(img, 'omega')
            img.save()
