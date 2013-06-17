# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Quiz'
        db.create_table(u'quiz_quiz', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('expected_return', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('expected_life', self.gf('django.db.models.fields.IntegerField')(default=60)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 17, 0, 0), auto_now_add=True, blank=True)),
            ('overlap', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
        ))
        db.send_create_signal(u'quiz', ['Quiz'])

        # Adding model 'Question'
        db.create_table(u'quiz_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discount_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=5)),
            ('years', self.gf('django.db.models.fields.IntegerField')()),
            ('start_amount', self.gf('django.db.models.fields.IntegerField')()),
            ('end_amount', self.gf('django.db.models.fields.IntegerField')()),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 17, 0, 0), auto_now_add=True, blank=True)),
            ('choice', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'quiz', ['Question'])

    def backwards(self, orm):
        # Deleting model 'Quiz'
        db.delete_table(u'quiz_quiz')

        # Deleting model 'Question'
        db.delete_table(u'quiz_question')

    models = {
        u'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'choice': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 17, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'discount_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '5'}),
            'end_amount': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Quiz']"}),
            'start_amount': ('django.db.models.fields.IntegerField', [], {}),
            'years': ('django.db.models.fields.IntegerField', [], {})
        },
        u'quiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 17, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'expected_life': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'expected_return': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overlap': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['quiz']