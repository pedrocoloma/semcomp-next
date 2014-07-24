# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Inscricao.CPF'
        db.add_column(u'website_inscricao', 'CPF',
                      self.gf('django.db.models.fields.CharField')(default=u'00000000000', max_length='11'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Inscricao.CPF'
        db.delete_column(u'website_inscricao', 'CPF')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'website.businesslecture': {
            'Meta': {'object_name': 'BusinessLecture'},
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'business_lecture'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['website.Company']", 'blank': 'True', 'unique': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Place']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'website.company': {
            'Meta': {'object_name': 'Company'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_fair': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'website.contactinformation': {
            'Meta': {'object_name': 'ContactInformation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Speaker']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'website.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Place']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slots': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['website.Event']", 'symmetrical': 'False'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Speaker']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'track': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'website.event': {
            'Meta': {'object_name': 'Event'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'#85144B'", 'max_length': '7'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'website.eventdata': {
            'Meta': {'object_name': 'EventData'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Place']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'slot': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['website.Event']", 'unique': 'True'})
        },
        u'website.inscricao': {
            'CPF': ('django.db.models.fields.CharField', [], {'max_length': "'11'"}),
            'Meta': {'object_name': 'Inscricao'},
            'avaliado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coffee': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comprovante': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'numero_documento': ('website.models.NullableCharField', [], {'max_length': "'30'", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'pagamento': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.SemcompUser']", 'primary_key': 'True'})
        },
        u'website.lecture': {
            'Meta': {'object_name': 'Lecture'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Place']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'slot': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['website.Event']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Speaker']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'website.place': {
            'Meta': {'object_name': 'Place'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '8'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '8'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'static_map': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'zoom': ('django.db.models.fields.IntegerField', [], {})
        },
        u'website.recruitmentprocess': {
            'Meta': {'object_name': 'RecruitmentProcess'},
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'recruitment_process'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['website.Company']", 'blank': 'True', 'unique': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Place']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'website.semcompconfig': {
            'Meta': {'object_name': 'SemcompConfig'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'value_bool': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        u'website.semcompuser': {
            'Meta': {'object_name': 'SemcompUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_usp': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'website.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['website']