# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table('nodes_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cn_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('cndb_uri', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('cndb_cached_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('pubkey', self.gf('django.db.models.fields.TextField')(unique=True, null=True, blank=True)),
            ('cert', self.gf('django.db.models.fields.TextField')(unique=True, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('arch', self.gf('django.db.models.fields.CharField')(default='x86_64', max_length=16)),
            ('local_iface', self.gf('django.db.models.fields.CharField')(default='eth0', max_length=16)),
            ('priv_ipv4_prefix', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
            ('sliver_mac_prefix', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=16, null=True, blank=True)),
            ('sliver_pub_ipv4_total', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('boot_sn', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('set_state', self.gf('django.db.models.fields.CharField')(default='install_conf', max_length=16)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('nodes', ['Node'])

        # Adding model 'NodeProp'
        db.create_table('nodes_nodeprop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nodes.Node'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('nodes', ['NodeProp'])

        # Adding unique constraint on 'NodeProp', fields ['node', 'name']
        db.create_unique('nodes_nodeprop', ['node_id', 'name'])

        # Adding model 'DirectIface'
        db.create_table('nodes_directiface', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nodes.Node'])),
        ))
        db.send_create_signal('nodes', ['DirectIface'])

        # Adding unique constraint on 'DirectIface', fields ['name', 'node']
        db.create_unique('nodes_directiface', ['name', 'node_id'])

        # Adding model 'Server'
        db.create_table('nodes_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cn_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('cndb_uri', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('cndb_cached_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('nodes', ['Server'])


    def backwards(self, orm):
        # Removing unique constraint on 'DirectIface', fields ['name', 'node']
        db.delete_unique('nodes_directiface', ['name', 'node_id'])

        # Removing unique constraint on 'NodeProp', fields ['node', 'name']
        db.delete_unique('nodes_nodeprop', ['node_id', 'name'])

        # Deleting model 'Node'
        db.delete_table('nodes_node')

        # Deleting model 'NodeProp'
        db.delete_table('nodes_nodeprop')

        # Deleting model 'DirectIface'
        db.delete_table('nodes_directiface')

        # Deleting model 'Server'
        db.delete_table('nodes_server')


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
        'nodes.directiface': {
            'Meta': {'unique_together': "(['name', 'node'],)", 'object_name': 'DirectIface'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nodes.Node']"})
        },
        'nodes.node': {
            'Meta': {'object_name': 'Node'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'arch': ('django.db.models.fields.CharField', [], {'default': "'x86_64'", 'max_length': '16'}),
            'boot_sn': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'cert': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cn_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'cndb_cached_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cndb_uri': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_iface': ('django.db.models.fields.CharField', [], {'default': "'eth0'", 'max_length': '16'}),
            'priv_ipv4_prefix': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'pubkey': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'set_state': ('django.db.models.fields.CharField', [], {'default': "'install_conf'", 'max_length': '16'}),
            'sliver_mac_prefix': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'sliver_pub_ipv4_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'nodes.nodeprop': {
            'Meta': {'unique_together': "(('node', 'name'),)", 'object_name': 'NodeProp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nodes.Node']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'nodes.server': {
            'Meta': {'object_name': 'Server'},
            'cn_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'cndb_cached_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cndb_uri': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tinc.gateway': {
            'Meta': {'object_name': 'Gateway'},
            'cn_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'cndb_cached_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cndb_uri': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tinc.island': {
            'Meta': {'object_name': 'Island'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'tinc.tincaddress': {
            'Meta': {'object_name': 'TincAddress'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'island': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tinc.Island']"}),
            'port': ('django.db.models.fields.SmallIntegerField', [], {'default': "'666'"}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tinc.TincServer']"})
        },
        'tinc.tincclient': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'TincClient'},
            'connect_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tinc.TincAddress']", 'symmetrical': 'False', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tinc.Island']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '36'}),
            'pubkey': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'tinc.tincserver': {
            'Meta': {'object_name': 'TincServer'},
            'connect_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tinc.TincAddress']", 'symmetrical': 'False', 'blank': 'True'}),
            'gateway': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tinc.Gateway']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pubkey': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['nodes']