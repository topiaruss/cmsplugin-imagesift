# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GalleryPlugin.thumbnail_geometry'
        db.add_column(u'imagesift_galleryplugin', 'thumbnail_geometry',
                      self.gf('django.db.models.fields.CharField')(default='50x50', max_length=50),
                      keep_default=False)

        # Adding field 'GalleryPlugin.image_geometry'
        db.add_column(u'imagesift_galleryplugin', 'image_geometry',
                      self.gf('django.db.models.fields.CharField')(default='300x200', max_length=50),
                      keep_default=False)

        # Adding field 'GalleryPlugin.thumbnail_limit'
        db.add_column(u'imagesift_galleryplugin', 'thumbnail_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GalleryPlugin.thumbnail_geometry'
        db.delete_column(u'imagesift_galleryplugin', 'thumbnail_geometry')

        # Deleting field 'GalleryPlugin.image_geometry'
        db.delete_column(u'imagesift_galleryplugin', 'image_geometry')

        # Deleting field 'GalleryPlugin.thumbnail_limit'
        db.delete_column(u'imagesift_galleryplugin', 'thumbnail_limit')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'imagesift.galleryplugin': {
            'Meta': {'object_name': 'GalleryPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'filter': ('django.db.models.fields.TextField', [], {}),
            'image_geometry': ('django.db.models.fields.CharField', [], {'default': "'300x200'", 'max_length': '50'}),
            'thumbnail_geometry': ('django.db.models.fields.CharField', [], {'default': "'50x50'", 'max_length': '50'}),
            'thumbnail_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['imagesift']