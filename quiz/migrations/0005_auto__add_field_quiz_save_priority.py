# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Quiz.save_priority'
        db.add_column(u'quiz_quiz', 'save_priority',
                      self.gf('django.db.models.fields.IntegerField')(default=4),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Quiz.save_priority'
        db.delete_column(u'quiz_quiz', 'save_priority')

    models = {
        u'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'choice': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 30, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'avg_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '5'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 30, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'expected_life': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'expected_return': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'net_worth': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'overlap': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'save_priority': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['quiz']