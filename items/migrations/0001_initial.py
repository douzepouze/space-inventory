# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'items_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['items.Location'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Person'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description_short', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('loc_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('label_created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'items', ['Location'])

        # Adding model 'LocationPhoto'
        db.create_table(u'items_locationphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('crop_from', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='locationphoto_related', null=True, to=orm['photologue.PhotoEffect'])),
            ('location', self.gf('mptt.fields.TreeForeignKey')(to=orm['items.Location'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'items', ['LocationPhoto'])

        # Adding model 'InventoryType'
        db.create_table(u'items_inventorytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['items.InventoryType'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'items', ['InventoryType'])

        # Adding model 'Inventory'
        db.create_table(u'items_inventory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(default='0')),
            ('consumable', self.gf('django.db.models.fields.BooleanField')()),
            ('movable', self.gf('django.db.models.fields.BooleanField')()),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('location', self.gf('mptt.fields.TreeForeignKey')(to=orm['items.Location'], null=True)),
            ('type', self.gf('mptt.fields.TreeForeignKey')(to=orm['items.InventoryType'])),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('availability', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('available_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('available_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('usage_appropriate', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('usage_inappropriate', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('usage_investigate', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('usage_alter', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('usage_takeaway', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('usage_exploit', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('usage_terms', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('mounted', self.gf('django.db.models.fields.BooleanField')()),
            ('location_hint', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('label_created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'items', ['Inventory'])

        # Adding model 'InventoryPhoto'
        db.create_table(u'items_inventoryphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('crop_from', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='inventoryphoto_related', null=True, to=orm['photologue.PhotoEffect'])),
            ('inventory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Inventory'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'items', ['InventoryPhoto'])

        # Adding model 'InventoryEquiptment'
        db.create_table(u'items_inventoryequiptment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='item', to=orm['items.Inventory'])),
            ('equiptment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equiptment', to=orm['items.Inventory'])),
            ('is_exclusive_equiptment', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'items', ['InventoryEquiptment'])

        # Adding model 'Person'
        db.create_table(u'items_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_extra_mid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_extra_bot', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('irc', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('wiki', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'items', ['Person'])

        # Adding M2M table for field groups on 'Person'
        m2m_table_name = db.shorten_name(u'items_person_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'items.person'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Person'
        m2m_table_name = db.shorten_name(u'items_person_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'items.person'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'permission_id'])

        # Adding model 'InventoryOwnershipResponsibility'
        db.create_table(u'items_inventoryownershipresponsibility', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Person'])),
            ('inventory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Inventory'])),
            ('is_owner', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'items', ['InventoryOwnershipResponsibility'])

        # Adding unique constraint on 'InventoryOwnershipResponsibility', fields ['person', 'inventory']
        db.create_unique(u'items_inventoryownershipresponsibility', ['person_id', 'inventory_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'InventoryOwnershipResponsibility', fields ['person', 'inventory']
        db.delete_unique(u'items_inventoryownershipresponsibility', ['person_id', 'inventory_id'])

        # Deleting model 'Location'
        db.delete_table(u'items_location')

        # Deleting model 'LocationPhoto'
        db.delete_table(u'items_locationphoto')

        # Deleting model 'InventoryType'
        db.delete_table(u'items_inventorytype')

        # Deleting model 'Inventory'
        db.delete_table(u'items_inventory')

        # Deleting model 'InventoryPhoto'
        db.delete_table(u'items_inventoryphoto')

        # Deleting model 'InventoryEquiptment'
        db.delete_table(u'items_inventoryequiptment')

        # Deleting model 'Person'
        db.delete_table(u'items_person')

        # Removing M2M table for field groups on 'Person'
        db.delete_table(db.shorten_name(u'items_person_groups'))

        # Removing M2M table for field user_permissions on 'Person'
        db.delete_table(db.shorten_name(u'items_person_user_permissions'))

        # Deleting model 'InventoryOwnershipResponsibility'
        db.delete_table(u'items_inventoryownershipresponsibility')


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
        u'items.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'accessories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'symmetrical': 'False', 'through': u"orm['items.InventoryEquiptment']", 'to': u"orm['items.Inventory']"}),
            'availability': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'available_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'available_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'consumable': ('django.db.models.fields.BooleanField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['items.Location']", 'null': 'True'}),
            'location_hint': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'mounted': ('django.db.models.fields.BooleanField', [], {}),
            'movable': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'persons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['items.Person']", 'through': u"orm['items.InventoryOwnershipResponsibility']", 'symmetrical': 'False'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['items.InventoryType']"}),
            'unique_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'usage_alter': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'usage_appropriate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'usage_exploit': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'usage_inappropriate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'usage_investigate': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'usage_takeaway': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'usage_terms': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': "'0'"})
        },
        u'items.inventoryequiptment': {
            'Meta': {'object_name': 'InventoryEquiptment'},
            'equiptment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'equiptment'", 'to': u"orm['items.Inventory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_exclusive_equiptment': ('django.db.models.fields.BooleanField', [], {}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item'", 'to': u"orm['items.Inventory']"})
        },
        u'items.inventoryownershipresponsibility': {
            'Meta': {'unique_together': "(('person', 'inventory'),)", 'object_name': 'InventoryOwnershipResponsibility'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Inventory']"}),
            'is_owner': ('django.db.models.fields.BooleanField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Person']"})
        },
        u'items.inventoryphoto': {
            'Meta': {'object_name': 'InventoryPhoto'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'inventoryphoto_related'", 'null': 'True', 'to': u"orm['photologue.PhotoEffect']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'inventory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Inventory']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'items.inventorytype': {
            'Meta': {'object_name': 'InventoryType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['items.InventoryType']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'items.location': {
            'Meta': {'object_name': 'Location'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_short': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'loc_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Person']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['items.Location']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'items.locationphoto': {
            'Meta': {'object_name': 'LocationPhoto'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locationphoto_related'", 'null': 'True', 'to': u"orm['photologue.PhotoEffect']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'location': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['items.Location']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'items.person': {
            'Meta': {'object_name': 'Person'},
            'address_extra_bot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_extra_mid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'irc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'wiki': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.6'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['items']