# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'website_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'website', ['Company'])

        # Adding model 'Place'
        db.create_table(u'website_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=8)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=8)),
            ('zoom', self.gf('django.db.models.fields.IntegerField')()),
            ('static_map', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'website', ['Place'])

        # Adding model 'Event'
        db.create_table(u'website_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('color', self.gf('django.db.models.fields.CharField')(default='#85144B', max_length=7)),
        ))
        db.send_create_signal(u'website', ['Event'])

        # Adding model 'EventData'
        db.create_table(u'website_eventdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['website.Event'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Place'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal(u'website', ['EventData'])

        # Adding model 'Speaker'
        db.create_table(u'website_speaker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'website', ['Speaker'])

        # Adding model 'ContactInformation'
        db.create_table(u'website_contactinformation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Speaker'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'website', ['ContactInformation'])

        # Adding model 'Lecture'
        db.create_table(u'website_lecture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['website.Event'], unique=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Place'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Speaker'], null=True, blank=True)),
        ))
        db.send_create_signal(u'website', ['Lecture'])

        # Adding model 'Course'
        db.create_table(u'website_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('track', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('requirements', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Place'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Speaker'], null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'website', ['Course'])

        # Adding M2M table for field slots on 'Course'
        m2m_table_name = db.shorten_name(u'website_course_slots')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'website.course'], null=False)),
            ('event', models.ForeignKey(orm[u'website.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'event_id'])

        # Adding model 'SemcompUser'
        db.create_table(u'website_semcompuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254, db_index=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('id_usp', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'website', ['SemcompUser'])

        # Adding M2M table for field groups on 'SemcompUser'
        m2m_table_name = db.shorten_name(u'website_semcompuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('semcompuser', models.ForeignKey(orm[u'website.semcompuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['semcompuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'SemcompUser'
        m2m_table_name = db.shorten_name(u'website_semcompuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('semcompuser', models.ForeignKey(orm[u'website.semcompuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['semcompuser_id', 'permission_id'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table(u'website_company')

        # Deleting model 'Place'
        db.delete_table(u'website_place')

        # Deleting model 'Event'
        db.delete_table(u'website_event')

        # Deleting model 'EventData'
        db.delete_table(u'website_eventdata')

        # Deleting model 'Speaker'
        db.delete_table(u'website_speaker')

        # Deleting model 'ContactInformation'
        db.delete_table(u'website_contactinformation')

        # Deleting model 'Lecture'
        db.delete_table(u'website_lecture')

        # Deleting model 'Course'
        db.delete_table(u'website_course')

        # Removing M2M table for field slots on 'Course'
        db.delete_table(db.shorten_name(u'website_course_slots'))

        # Deleting model 'SemcompUser'
        db.delete_table(u'website_semcompuser')

        # Removing M2M table for field groups on 'SemcompUser'
        db.delete_table(db.shorten_name(u'website_semcompuser_groups'))

        # Removing M2M table for field user_permissions on 'SemcompUser'
        db.delete_table(db.shorten_name(u'website_semcompuser_user_permissions'))


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
        u'website.company': {
            'Meta': {'object_name': 'Company'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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