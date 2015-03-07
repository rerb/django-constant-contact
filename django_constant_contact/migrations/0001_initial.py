# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailMarketingCampaign'
        db.create_table(u'django_constant_contact_emailmarketingcampaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('django_constant_contact_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'django_constant_contact', ['EmailMarketingCampaign'])


    def backwards(self, orm):
        # Deleting model 'EmailMarketingCampaign'
        db.delete_table(u'django_constant_contact_emailmarketingcampaign')


    models = {
        u'django_constant_contact.emailmarketingcampaign': {
            'Meta': {'object_name': 'EmailMarketingCampaign'},
            'django_constant_contact_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['django_constant_contact']
