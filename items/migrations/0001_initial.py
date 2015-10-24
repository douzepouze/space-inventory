# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import photologue.models
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import items.models
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0008_auto_20150509_1557'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(help_text=b'ex: Miezekatze', max_length=255, verbose_name=b'Nickname')),
                ('street', models.CharField(help_text='ex: Heilmannstra&szlig;e 30', max_length=255, verbose_name=b'Street', blank=True)),
                ('address_extra_mid', models.CharField(help_text=b'ex: c/o the best of the best, sir', max_length=255, verbose_name=b'Address Extra Mid', blank=True)),
                ('zip_code', models.CharField(help_text=b'ex: 82049', max_length=255, verbose_name=b'Zip Code', blank=True)),
                ('city', models.CharField(help_text=b'ex: Pullach', max_length=255, verbose_name=b'City', blank=True)),
                ('state', models.CharField(help_text=b'ex: Oberbayern', max_length=255, verbose_name=b'State', blank=True)),
                ('country', models.CharField(help_text=b'ex: Germany', max_length=255, verbose_name=b'Country', blank=True)),
                ('address_extra_bot', models.CharField(help_text=b'ex: aint no kiddin', max_length=255, verbose_name=b'Address Extra Bottom', blank=True)),
                ('info', models.CharField(help_text=b'ex: Miep Miep', max_length=255, verbose_name=b'Info', blank=True)),
                ('irc', models.CharField(help_text=b'ex: #cccac@irc.hackint.eu', max_length=255, verbose_name=b'IRC', blank=True)),
                ('jabber', models.CharField(help_text=b'ex: miezekatze@jabber.ccc.de', max_length=255, verbose_name=b'Jabber', blank=True)),
                ('phone', models.CharField(help_text=b'ex: 0049 1234 677899', max_length=255, verbose_name=b'Phone', blank=True)),
                ('wiki', models.CharField(help_text=b'ex: URL to ur spaces wiki account/main page', max_length=255, verbose_name=b'Wiki', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unique_name', models.CharField(help_text=b'ex: Rigol Electronics DS1102E DSO', max_length=255, verbose_name=b'unique name')),
                ('manufacturer', models.CharField(help_text=b'ex: Rigol Electronics', max_length=255, verbose_name=b'manufacturer', blank=True)),
                ('name', models.CharField(help_text=b'ex: DS1102E', max_length=255, verbose_name=b'product name', blank=True)),
                ('value', models.IntegerField(default=b'0', help_text=b'ex: 370 <i>&euro;</i>', verbose_name=b'monetary value')),
                ('consumable', models.BooleanField(help_text=b'ex: an resistor usually is consumable, an oscilloscope usually not.')),
                ('movable', models.BooleanField(help_text=b'movable in the sense of one can carry it. ex: oscilloscope: movable, giant roaring fridge: unmovable')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name=b'UUID', editable=False, blank=True)),
                ('serial', models.CharField(max_length=255, verbose_name=b'Serial Number/String', blank=True)),
                ('condition', models.CharField(default=b'FUNC', max_length=100, choices=[(b'FUNC', b'Functional'), (b'LIMITED_FUNC', b'Limited Functional'), (b'UNFUNCT', b'Unfunctional'), (b'REPAIR', b'In Reparation'), (b'BRICKED', b'Bricked'), (b'DISPOSED', b'Disposed')])),
                ('availability', models.CharField(default=b'UNLIMITED', max_length=100, choices=[(b'UNLIMITED', b'Unlimited'), (b'LIMITED', b'Limited'), (b'UNAVAILABLE', b'Unavailable')])),
                ('available_from', models.DateField(null=True, blank=True)),
                ('available_to', models.DateField(null=True, blank=True)),
                ('usage_appropriate', models.CharField(default=b'YES', max_length=255, choices=[(b'YES', b'OK for everybody'), (b'NO', b"Don't even think about it..."), (b'ASK', b'Ask'), (b'WITHINSPACE', b'Within the Hackerspace')])),
                ('usage_inappropriate', models.CharField(default=b'ASK', max_length=255, choices=[(b'YES', b'OK for everybody'), (b'NO', b"Don't even think about it..."), (b'ASK', b'Ask'), (b'WITHINSPACE', b'Within the Hackerspace')])),
                ('usage_investigate', models.CharField(default=b'ASK', max_length=255, choices=[(b'YES', b'OK for everybody'), (b'NO', b"Don't even think about it..."), (b'ASK', b'Ask'), (b'WITHINSPACE', b'Within the Hackerspace')])),
                ('usage_alter', models.CharField(default=b'ASK', max_length=255, choices=[(b'YES', b'OK for everybody'), (b'NO', b"Don't even think about it..."), (b'ASK', b'Ask'), (b'WITHINSPACE', b'Within the Hackerspace')])),
                ('usage_takeaway', models.CharField(default=b'NO', max_length=255, choices=[(b'YES', b'OK for everybody'), (b'NO', b"Don't even think about it..."), (b'ASK', b'Ask'), (b'WITHINSPACE', b'Within the Hackerspace')])),
                ('usage_exploit', models.CharField(default=b'NO', max_length=255, choices=[(b'YES', b'OK for everybody'), (b'NO', b"Don't even think about it..."), (b'ASK', b'Ask'), (b'WITHINSPACE', b'Within the Hackerspace')])),
                ('usage_terms', models.TextField(blank=True)),
                ('mounted', models.BooleanField()),
                ('location_hint', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(blank=True)),
                ('label_created', models.DateTimeField(null=True, editable=False, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryOwnershipResponsibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField()),
                ('inventory', models.ForeignKey(to='items.Inventory')),
                ('person', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=photologue.models.get_storage_path, verbose_name='image')),
                ('date_taken', models.DateTimeField(verbose_name='date taken', null=True, editable=False, blank=True)),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='view count', editable=False)),
                ('crop_from', models.CharField(default=b'center', max_length=10, verbose_name='crop from', blank=True, choices=[(b'top', 'Top'), (b'right', 'Right'), (b'bottom', 'Bottom'), (b'left', 'Left'), (b'center', 'Center (Default)')])),
                ('title', models.CharField(max_length=50, verbose_name='title', blank=True)),
                ('caption', models.TextField(verbose_name='caption', blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
                ('effect', models.ForeignKey(related_name='inventoryphoto_related', verbose_name='effect', blank=True, to='photologue.PhotoEffect', null=True)),
                ('inventory', models.ForeignKey(to='items.Inventory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Ex: Digital Storage Oscilosope', max_length=255, verbose_name=b'Inventory Type')),
                ('description', models.TextField(blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='items.InventoryType', help_text=b'', null=True, verbose_name=b'Is subtype of ')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, items.models.MPTTModelMixin),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Ex: Someones Crate', max_length=255, verbose_name=b'Location Name')),
                ('description_short', models.CharField(help_text=b'Short description whats in the crate. Used for labels and stuff.', max_length=255, verbose_name=b'Description (Brief)')),
                ('description', models.TextField(blank=True)),
                ('loc_type', models.CharField(max_length=255, verbose_name=b'Location Type', choices=[(b'CRATE', b'Crate'), (b'SHELF', b'Shelf'), (b'ROOM', b'Room'), (b'MAGAZINE', b'Magazine')])),
                ('uuid', models.UUIDField(verbose_name=b'UUID', editable=False, blank=True)),
                ('label_created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name=b'Is stored in ', blank=True, to='items.Location', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, items.models.MPTTModelMixin),
        ),
        migrations.CreateModel(
            name='LocationPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=photologue.models.get_storage_path, verbose_name='image')),
                ('date_taken', models.DateTimeField(verbose_name='date taken', null=True, editable=False, blank=True)),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='view count', editable=False)),
                ('crop_from', models.CharField(default=b'center', max_length=10, verbose_name='crop from', blank=True, choices=[(b'top', 'Top'), (b'right', 'Right'), (b'bottom', 'Bottom'), (b'left', 'Left'), (b'center', 'Center (Default)')])),
                ('title', models.CharField(max_length=50, verbose_name='title', blank=True)),
                ('caption', models.TextField(verbose_name='caption', blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
                ('effect', models.ForeignKey(related_name='locationphoto_related', verbose_name='effect', blank=True, to='photologue.PhotoEffect', null=True)),
                ('location', mptt.fields.TreeForeignKey(to='items.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='inventory',
            name='location',
            field=mptt.fields.TreeForeignKey(to='items.Location', null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='persons',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='items.InventoryOwnershipResponsibility'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='related_items',
            field=models.ManyToManyField(related_name='_related_items_+', to='items.Inventory', blank=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='type',
            field=mptt.fields.TreeForeignKey(to='items.InventoryType'),
        ),
        migrations.AlterUniqueTogether(
            name='inventoryownershipresponsibility',
            unique_together=set([('person', 'inventory')]),
        ),
    ]
