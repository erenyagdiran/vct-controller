# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Node', fields ['hostname']
        db.delete_unique('nodes_node', ['hostname'])

        # Adding model 'Island'
        db.create_table('nodes_island', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('nodes', ['Island'])

        # Adding field 'Node.island'
        db.add_column('nodes_node', 'island',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nodes.Island'], null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'Island'
        db.delete_table('nodes_island')

        # Deleting field 'Node.island'
        db.delete_column('nodes_node', 'island_id')

        # Adding unique constraint on 'Node', fields ['hostname']
        db.create_unique('nodes_node', ['hostname'])

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nodes.cpu': {
            'Meta': {'object_name': 'CPU'},
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nodes.Node']", 'unique': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': "'1'", 'null': 'True', 'blank': 'True'})
        },
        'nodes.deleterequest': {
            'Meta': {'object_name': 'DeleteRequest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nodes.Node']"})
        },
        'nodes.interface': {
            'Meta': {'object_name': 'Interface'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nodes.Node']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'802.11a/b/g/n'", 'max_length': '255'})
        },
        'nodes.island': {
            'Meta': {'object_name': 'Island'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'nodes.memory': {
            'Meta': {'object_name': 'Memory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nodes.Node']", 'unique': 'True'}),
            'size': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'nodes.node': {
            'Meta': {'object_name': 'Node'},
            'architecture': ('django.db.models.fields.CharField', [], {'default': "'x86_generic'", 'max_length': '128'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'island': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nodes.Island']", 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'public_key': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'ONLINE'", 'max_length': '32'}),
            'uci': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'nodes.storage': {
            'Meta': {'object_name': 'Storage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nodes.Node']", 'unique': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'types': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['nodes']