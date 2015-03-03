# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailMarketingCampaign'
        db.create_table(u'constant_contact_emailmarketingcampaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('constant_contact_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'constant_contact', ['EmailMarketingCampaign'])


    def backwards(self, orm):
        # Deleting model 'EmailMarketingCampaign'
        db.delete_table(u'constant_contact_emailmarketingcampaign')


    models = {
        u'constant_contact.emailmarketingcampaign': {
            'Meta': {'object_name': 'EmailMarketingCampaign'},
            'constant_contact_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['constant_contact']