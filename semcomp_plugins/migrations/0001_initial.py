# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MultiColumns'
        db.create_table(u'semcomp_plugins_multicolumns', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'semcomp_plugins', ['MultiColumns'])

        # Adding model 'Column'
        db.create_table(u'semcomp_plugins_column', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('small_width', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('large_width', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('custom_classes', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal(u'semcomp_plugins', ['Column'])

        # Adding model 'MinicursosPluginModel'
        db.create_table(u'semcomp_plugins_minicursospluginmodel', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('columns_small', self.gf('django.db.models.fields.IntegerField')()),
            ('columns_medium', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('columns_large', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'semcomp_plugins', ['MinicursosPluginModel'])


    def backwards(self, orm):
        # Deleting model 'MultiColumns'
        db.delete_table(u'semcomp_plugins_multicolumns')

        # Deleting model 'Column'
        db.delete_table(u'semcomp_plugins_column')

        # Deleting model 'MinicursosPluginModel'
        db.delete_table(u'semcomp_plugins_minicursospluginmodel')


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
        u'semcomp_plugins.column': {
            'Meta': {'object_name': 'Column', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'custom_classes': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'large_width': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'small_width': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        u'semcomp_plugins.minicursospluginmodel': {
            'Meta': {'object_name': 'MinicursosPluginModel', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'columns_large': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'columns_medium': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'columns_small': ('django.db.models.fields.IntegerField', [], {})
        },
        u'semcomp_plugins.multicolumns': {
            'Meta': {'object_name': 'MultiColumns', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['semcomp_plugins']