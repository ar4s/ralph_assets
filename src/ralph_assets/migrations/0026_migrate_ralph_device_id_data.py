# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    no_dry_run = True

    def forwards(self, orm):
        for dev in orm['ralph_assets.deviceinfo'].objects.all():
            if dev.ralph_device_id_old:
                try:
                    dev.ralph_device = orm['discovery.device'].objects.get(
                        pk=dev.ralph_device_id_old
                    )
                    dev.save()
                except Exception as e:
                    print(e)

    def backwards(self, orm):
        for dev in orm['ralph_assets.deviceinfo'].objects.all():
            if dev.ralph_device:
                try:
                    dev.ralph_device_id_old = dev.ralph_device.id
                    dev.save()
                except Exception as e:
                    print(e)

    models = {
        'account.profile': {
            'Meta': {'object_name': 'Profile'},
            'activation_token': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '40', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'cost_center': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'country': ('django.db.models.fields.PositiveIntegerField', [], {'default': '153'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'employee_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'gender': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'home_page': (u'dj.choices.fields.ChoiceField', [], {'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'blank': 'False', u'default': '1', 'null': 'False', '_in_south': 'True', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_active': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '30', 'blank': 'True'}),
            'profit_center': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'segment': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'account.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'profile': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['account.Profile']", 'symmetrical': 'False'})
        },
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
        'business.businesssegment': {
            'Meta': {'object_name': 'BusinessSegment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'business.department': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Department'},
            'icon': (u'dj.choices.fields.ChoiceField', [], {'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'blank': 'True', u'default': 'None', 'null': 'True', '_in_south': 'True', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'business.profitcenter': {
            'Meta': {'object_name': 'ProfitCenter'},
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'business.venture': {
            'Meta': {'ordering': "(u'parent__symbol', u'symbol')", 'unique_together': "((u'parent', u'symbol'),)", 'object_name': 'Venture'},
            'business_segment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['business.BusinessSegment']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'data_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discovery.DataCenter']", 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['business.Department']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_infrastructure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'margin_kind': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['discovery.MarginKind']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'child_set'", 'null': 'True', 'blank': 'True', 'to': "orm['business.Venture']"}),
            'path': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'preboot': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['deployment.Preboot']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'profit_center': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['business.ProfitCenter']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'show_in_ralph': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'symbol': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '32', 'blank': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'business.venturerole': {
            'Meta': {'ordering': "(u'parent__name', u'name')", 'unique_together': "((u'name', u'venture'),)", 'object_name': 'VentureRole'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'child_set'", 'null': 'True', 'blank': 'True', 'to': "orm['business.VentureRole']"}),
            'path': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'preboot': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['deployment.Preboot']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'venture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['business.Venture']"})
        },
        'cmdb.ci': {
            'Meta': {'unique_together': "((u'content_type', u'object_id'),)", 'object_name': 'CI'},
            'added_manually': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'barcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'business_service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cmdb.CILayer']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cmdb.CIOwner']", 'through': "orm['cmdb.CIOwnership']", 'symmetrical': 'False'}),
            'pci_scope': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cmdb.CI']", 'through': "orm['cmdb.CIRelation']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '11'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2', 'max_length': '11'}),
            'technical_service': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmdb.CIType']"}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'zabbix_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'cmdb.cilayer': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'CILayer'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'connected_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cmdb.CIType']", 'symmetrical': 'False', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'icon': (u'dj.choices.fields.ChoiceField', [], {'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'blank': 'True', u'default': 'None', 'null': 'True', '_in_south': 'True', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cmdb.ciowner': {
            'Meta': {'object_name': 'CIOwner'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['account.Profile']", 'unique': 'True'})
        },
        'cmdb.ciownership': {
            'Meta': {'object_name': 'CIOwnership'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ci': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmdb.CI']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmdb.CIOwner']"}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'cmdb.cirelation': {
            'Meta': {'unique_together': "((u'parent', u'child', u'type'),)", 'object_name': 'CIRelation'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'child'", 'to': "orm['cmdb.CI']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'parent'", 'to': "orm['cmdb.CI']"}),
            'readonly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '11'})
        },
        'cmdb.citype': {
            'Meta': {'object_name': 'CIType'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'icon_class': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'deployment.preboot': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Preboot'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['deployment.PrebootFile']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'deployment.prebootfile': {
            'Meta': {'object_name': 'PrebootFile'},
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ftype': (u'dj.choices.fields.ChoiceField', [], {'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'blank': 'False', u'default': '101', 'null': 'False', '_in_south': 'True', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'raw_config': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'discovery.connection': {
            'Meta': {'object_name': 'Connection'},
            'connection_type': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbound': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'inbound_connections'", 'on_delete': 'models.PROTECT', 'to': "orm['discovery.Device']"}),
            'outbound': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'outbound_connections'", 'on_delete': 'models.PROTECT', 'to': "orm['discovery.Device']"})
        },
        'discovery.datacenter': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'DataCenter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'discovery.deprecationkind': {
            'Meta': {'object_name': 'DeprecationKind'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'months': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'})
        },
        'discovery.device': {
            'Meta': {'object_name': 'Device'},
            'barcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'boot_firmware': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cached_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cached_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'chassis_position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'connections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['discovery.Device']", 'through': "orm['discovery.Connection']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dc': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'deprecation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deprecation_kind': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['discovery.DeprecationKind']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'device_environment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'device'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['cmdb.CI']"}),
            'diag_firmware': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hard_firmware': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'logical_parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'logicalchild_set'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['discovery.Device']", 'blank': 'True', 'null': 'True'}),
            'management': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'managed_set'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['discovery.IPAddress']", 'blank': 'True', 'null': 'True'}),
            'margin_kind': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['discovery.MarginKind']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'max_save_priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'mgmt_firmware': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'device_set'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['discovery.DeviceModel']", 'blank': 'True', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'child_set'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['discovery.Device']", 'blank': 'True', 'null': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rack': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'save_priorities': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'device'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['cmdb.CI']"}),
            'sn': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'support_expiration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'support_kind': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'uptime_seconds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'uptime_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'venture': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['business.Venture']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'venture_role': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['business.VentureRole']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'warranty_expiration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'discovery.devicemodel': {
            'Meta': {'object_name': 'DeviceModel'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'chassis_size': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_save_priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'save_priorities': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '401'})
        },
        'discovery.discoveryqueue': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'DiscoveryQueue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'discovery.environment': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Environment'},
            'data_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discovery.DataCenter']"}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hosts_naming_template': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'next_server': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '32', 'blank': 'True'}),
            'queue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discovery.DiscoveryQueue']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'discovery.ipaddress': {
            'Meta': {'object_name': 'IPAddress'},
            'address': ('django.db.models.fields.IPAddressField', [], {'default': 'None', 'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dead_ping_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['discovery.Device']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'dns_info': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'http_family': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_buried': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_management': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_plugins': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_puppet': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['discovery.Network']", 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'scan_summary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scan.ScanSummary']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'snmp_community': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'snmp_name': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'snmp_version': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'venture': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['business.Venture']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'discovery.marginkind': {
            'Meta': {'object_name': 'MarginKind'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'margin': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'})
        },
        'discovery.network': {
            'Meta': {'ordering': "(u'vlan',)", 'object_name': 'Network'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '18'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'custom_dns_servers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dnsedit.DNSServer']", 'null': 'True', 'blank': 'True'}),
            'data_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discovery.DataCenter']", 'null': 'True', 'blank': 'True'}),
            'dhcp_broadcast': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'dhcp_config': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discovery.Environment']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'gateway': ('django.db.models.fields.IPAddressField', [], {'default': 'None', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'gateway_as_int': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_addresses': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['discovery.NetworkKind']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'last_scan': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'max_ip': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'min_ip': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'racks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['discovery.Device']", 'symmetrical': 'False'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'reserved': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'reserved_top_margin': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'terminators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['discovery.NetworkTerminator']", 'symmetrical': 'False'}),
            'vlan': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'discovery.networkkind': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'NetworkKind'},
            'icon': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'discovery.networkterminator': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'NetworkTerminator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'dnsedit.dnsserver': {
            'Meta': {'object_name': 'DNSServer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'ralph_assets.accessory': {
            'Meta': {'object_name': 'Accessory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.action': {
            'Meta': {'object_name': 'Action'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.asset': {
            'Meta': {'object_name': 'Asset'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'parents'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['ralph_assets.Attachment']"}),
            'barcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'budget_info': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ralph_assets.BudgetInfo']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'delivery_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deprecation_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deprecation_rate': ('django.db.models.fields.DecimalField', [], {'default': '25', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'device_environment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['cmdb.CI']", 'null': 'True', 'on_delete': 'models.PROTECT'}),
            'device_info': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ralph_assets.DeviceInfo']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'force_deprecation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hostname': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '16', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'loan_end_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'assets'", 'on_delete': 'models.PROTECT', 'to': "orm['ralph_assets.AssetModel']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'niw': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'office_info': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ralph_assets.OfficeInfo']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'order_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'owner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'part_info': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ralph_assets.PartInfo']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'production_use_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'production_year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'property_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetOwner']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'provider_order_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_order': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Region']"}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'request_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'required_support': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['cmdb.CI']", 'null': 'True', 'on_delete': 'models.PROTECT'}),
            'service_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Service']", 'null': 'True', 'blank': 'True'}),
            'slots': ('django.db.models.fields.FloatField', [], {'default': '0', 'max_length': '64'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'support_period': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'support_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'support_type': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'support_void_reporting': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'task_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Warehouse']", 'on_delete': 'models.PROTECT'})
        },
        'ralph_assets.assetcategory': {
            'Meta': {'object_name': 'AssetCategory'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '4', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'is_blade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': "orm['ralph_assets.AssetCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'ralph_assets.assetlasthostname': {
            'Meta': {'unique_together': "((u'prefix', u'postfix'),)", 'object_name': 'AssetLastHostname'},
            'counter': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postfix': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'})
        },
        'ralph_assets.assetmanufacturer': {
            'Meta': {'object_name': 'AssetManufacturer'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.assetmodel': {
            'Meta': {'object_name': 'AssetModel'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'models'", 'null': 'True', 'to': "orm['ralph_assets.AssetCategory']"}),
            'cores_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'height_of_device': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetManufacturer']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'power_consumption': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'visualization_layout_back': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'}),
            'visualization_layout_front': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'})
        },
        'ralph_assets.assetowner': {
            'Meta': {'object_name': 'AssetOwner'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'ralph_assets.budgetinfo': {
            'Meta': {'object_name': 'BudgetInfo'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.coaoemos': {
            'Meta': {'object_name': 'CoaOemOs'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.datacenter': {
            'Meta': {'object_name': 'DataCenter'},
            'deprecated_ralph_dc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discovery.Device']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'visualization_cols_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'visualization_rows_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'})
        },
        'ralph_assets.deviceinfo': {
            'Meta': {'object_name': 'DeviceInfo'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'data_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.DataCenter']", 'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'orientation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Rack']", 'null': 'True', 'blank': 'True'}),
            'rack_old': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'ralph_device': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': "orm['discovery.Device']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'ralph_device_id_old': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'server_room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.ServerRoom']", 'null': 'True'}),
            'slot_no': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'u_height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'u_level': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'ralph_assets.history': {
            'Meta': {'ordering': "(u'-date',)", 'object_name': 'History'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'field_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_value': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'old_value': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'ralph_assets.importproblem': {
            'Meta': {'object_name': 'ImportProblem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'severity': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'ralph_assets.licence': {
            'Meta': {'object_name': 'Licence'},
            'accounting_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'asset_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'licences'", 'symmetrical': 'False', 'through': u"orm['ralph_assets.LicenceAsset']", 'to': "orm['ralph_assets.Asset']"}),
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ralph_assets.Attachment']", 'null': 'True', 'blank': 'True'}),
            'budget_info': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ralph_assets.BudgetInfo']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'licence_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ralph_assets.LicenceType']", 'on_delete': 'models.PROTECT'}),
            'license_details': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '1024', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetManufacturer']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'niw': ('django.db.models.fields.CharField', [], {'default': "u'N/A'", 'unique': 'True', 'max_length': '200'}),
            'number_bought': ('django.db.models.fields.IntegerField', [], {}),
            'order_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['ralph_assets.Licence']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'property_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetOwner']", 'null': 'True', 'on_delete': 'models.PROTECT'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Region']"}),
            'remarks': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'service_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Service']", 'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'software_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ralph_assets.SoftwareCategory']", 'on_delete': 'models.PROTECT'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': u"orm['ralph_assets.LicenceUser']", 'symmetrical': 'False'}),
            'valid_thru': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ralph_assets.licenceasset': {
            'Meta': {'unique_together': "((u'licence', u'asset'),)", 'object_name': 'LicenceAsset'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Asset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ralph_assets.Licence']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'ralph_assets.licencetype': {
            'Meta': {'object_name': 'LicenceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        u'ralph_assets.licenceuser': {
            'Meta': {'unique_together': "((u'licence', u'user'),)", 'object_name': 'LicenceUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ralph_assets.Licence']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'licences'", 'to': "orm['auth.User']"})
        },
        'ralph_assets.officeinfo': {
            'Meta': {'object_name': 'OfficeInfo'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'coa_number': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'coa_oem_os': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.CoaOemOs']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'max_length': '18', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'license_key': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'purpose': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'ralph_assets.partinfo': {
            'Meta': {'object_name': 'PartInfo'},
            'barcode_salvaged': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'device'", 'null': 'True', 'to': "orm['ralph_assets.Asset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'source_device': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'source_device'", 'null': 'True', 'to': "orm['ralph_assets.Asset']"})
        },
        'ralph_assets.rack': {
            'Meta': {'unique_together': "((u'name', u'data_center'),)", 'object_name': 'Rack'},
            'accessories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ralph_assets.Accessory']", 'through': "orm['ralph_assets.RackAccessory']", 'symmetrical': 'False'}),
            'data_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.DataCenter']"}),
            'deprecated_ralph_rack': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'deprecated_asset_rack'", 'null': 'True', 'to': "orm['discovery.Device']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_u_height': ('django.db.models.fields.IntegerField', [], {'default': '48'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'orientation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'server_room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.ServerRoom']", 'null': 'True', 'blank': 'True'}),
            'visualization_col': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'visualization_row': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'ralph_assets.rackaccessory': {
            'Meta': {'object_name': 'RackAccessory'},
            'accessory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Accessory']"}),
            'data_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.DataCenter']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orientation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Rack']"}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'server_room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.ServerRoom']", 'null': 'True'})
        },
        'ralph_assets.reportodtsource': {
            'Meta': {'object_name': 'ReportOdtSource'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ralph_assets.reportodtsourcelanguage': {
            'Meta': {'unique_together': "((u'language', u'report_odt_source'),)", 'object_name': 'ReportOdtSourceLanguage'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'report_odt_source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'odt_templates'", 'to': "orm['ralph_assets.ReportOdtSource']"}),
            'template': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'ralph_assets.serverroom': {
            'Meta': {'object_name': 'ServerRoom'},
            'data_center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.DataCenter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        'ralph_assets.service': {
            'Meta': {'object_name': 'Service'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cost_center': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'profit_center': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'})
        },
        u'ralph_assets.softwarecategory': {
            'Meta': {'object_name': 'SoftwareCategory'},
            'asset_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.support': {
            'Meta': {'object_name': 'Support'},
            'additional_notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'asset_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'supports'", 'symmetrical': 'False', 'to': "orm['ralph_assets.Asset']"}),
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ralph_assets.Attachment']", 'null': 'True', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'contract_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contract_terms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'date_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'escalation_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'period_in_months': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'property_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetOwner']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Region']"}),
            'serial_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sla_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'supplier': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'support_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ralph_assets.SupportType']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'ralph_assets.supporttype': {
            'Meta': {'object_name': 'SupportType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.transition': {
            'Meta': {'object_name': 'Transition'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ralph_assets.Action']", 'symmetrical': 'False'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'required_report': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'to_status': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'ralph_assets.transitionshistory': {
            'Meta': {'ordering': "[u'-created']", 'object_name': 'TransitionsHistory'},
            'affected_user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'affected_user_transition_histories'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ralph_assets.Asset']", 'symmetrical': 'False'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logged_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'logged_user_transition_histories'", 'to': "orm['auth.User']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'report_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'report_filename': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'transition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Transition']"}),
            'uid': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True', 'blank': 'True'})
        },
        'ralph_assets.warehouse': {
            'Meta': {'object_name': 'Warehouse'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'scan.scansummary': {
            'Meta': {'object_name': 'ScanSummary'},
            'changed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_checksum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'false_positive_checksum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'previous_checksum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Profile']"}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'tags_tag_tags'", 'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.PositiveIntegerField', [], {'default': '39'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'official': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stem': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'related_tags'", 'null': 'True', 'to': "orm['tags.TagStem']"})
        },
        'tags.tagstem': {
            'Meta': {'object_name': 'TagStem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.PositiveIntegerField', [], {'default': '39'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'tag_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['ralph_assets']
    symmetrical = True
