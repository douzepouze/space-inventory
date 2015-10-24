# -*- coding: utf-8 -*-
#
#  Some code was taken from  EAV-Django Copyright © 2009—2010  Andrey Mikhaylenko
#

# Python Imports
import uuid

# Django Imports
from django.db import models
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.core.urlresolvers import reverse

# 3rd Party Imports
from mptt.models import MPTTModel, TreeForeignKey
from photologue.models import ImageModel


# South Rules
# add_introspection_rules([
# (
#     [models.CharField], # Class(es) these apply to
#     [],         # Positional arguments (not used)
#     {           # Keyword argument
#         "default": ["default", {"ignore_if": "default"}],
#     },
# ),
# ], ["^items\.(Location|Inventory)\.fields\.uuid"])


class MPTTModelMixin(object):
    def get_ancestors_self(self):
        return self.get_ancestors(include_self=True)


class Location(MPTTModel, MPTTModelMixin):
    parent = TreeForeignKey('self',
                            null=True,
                            blank=True,
                            related_name='children',
                            verbose_name="Is stored in ",
                            )
    owner = models.ForeignKey('Person')
    
    # Location Types
    TYPE_CRATE = 'CRATE'
    TYPE_SHELF = 'SHELF'
    TYPE_ROOM = 'ROOM'
    TYPE_MAGAZINE = 'MAGAZINE'
    
    LOCATION_CHOICES = (
        (TYPE_CRATE, 'Crate'),
        (TYPE_SHELF, 'Shelf'),
        (TYPE_ROOM, 'Room'),
        (TYPE_MAGAZINE, 'Magazine')
    )
    
    name = models.CharField("Location Name", help_text="Ex: Someones Crate", max_length=255)
    description_short = models.CharField("Description (Brief)",
                                         help_text="Short description whats in the crate. Used for labels and stuff.",
                                         max_length=255)
    description = models.TextField(blank=True)
    loc_type = models.CharField("Location Type", choices=LOCATION_CHOICES, max_length=255)
    uuid = models.UUIDField('UUID', default=uuid.uuid4, blank=True, editable=False)

    # TODO Remove in future, when "labels" app is created ...
    label_created = models.DateTimeField(blank=True, editable=False, null=True)

    def get_absolute_url(self):
        return reverse('items:location_show', args=[str(self.uuid)])

    def __unicode__(self):
        return self.name


class LocationPhoto(ImageModel):
    location = TreeForeignKey(Location)
    title = models.CharField(_('title'),
                             max_length=50,
                             blank=True)
    caption = models.TextField(_('caption'),
                               blank=True)
    date_added = models.DateTimeField(_('date added'),
                                    default=now)

    def __unicode__(self):
        if not self.title:
            return unicode(self.image)
        else:
            return self.title


class InventoryType(MPTTModel, MPTTModelMixin):
    name = models.CharField(
        'Inventory Type',
        help_text="Ex: Digital Storage Oscilosope",
        max_length=255
    )

    # fixme: Catch loop self referencing
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name="Is subtype of ",
        help_text="",
        related_name='children'
    )
    
    description = models.TextField(blank=True)
     
    def __unicode__(self):
        return self.name


class Inventory(models.Model):
    unique_name = models.CharField(
        'unique name',
        help_text='ex: Rigol Electronics DS1102E DSO',
        max_length=255
    )
    
    manufacturer = models.CharField(
        'manufacturer',
        help_text='ex: Rigol Electronics',
        blank=True,
        max_length=255
    )
    
    name = models.CharField(
        'product name',
        help_text='ex: DS1102E',
        blank=True,
        max_length=255
    )
    
    value = models.IntegerField(
        'monetary value',
        help_text='ex: 370 <i>&euro;</i>',
        default='0'
    )
    
    consumable = models.BooleanField(
        help_text='ex: an resistor usually is consumable, an oscilloscope usually not.'
    )
    
    movable = models.BooleanField(
        help_text='movable in the sense of one can carry it. ex: oscilloscope: movable, giant roaring fridge: unmovable'
    )

    uuid = models.UUIDField(
        'UUID',
        default=uuid.uuid4,
        blank=True,
        editable=False
    )
    
    serial = models.CharField(
        'Serial Number/String',
        max_length=255,
        blank=True
    )
    
    persons = models.ManyToManyField(
        'Person',
        through='InventoryOwnershipResponsibility'
    )
    
    location = TreeForeignKey(Location, null=True)
    
    type = TreeForeignKey(InventoryType)

    related_items = models.ManyToManyField("self", blank=True)
    
    # Condition
    COND_FUNCT = 'FUNC'
    COND_LMD_FUNCT = 'LIMITED_FUNC'
    COND_UNFUNCT = 'UNFUNCT'
    COND_REPAIR = 'REPAIR'
    COND_BRICKED = 'BRICKED'
    COND_DISPOSED = 'DISPOSED'
    CONDITION_CHOICES = (
        (COND_FUNCT, 'Functional'),
        (COND_LMD_FUNCT, 'Limited Functional'),
        (COND_UNFUNCT, 'Unfunctional'),
        (COND_REPAIR, 'In Reparation'),
        (COND_BRICKED, 'Bricked'),
        (COND_DISPOSED, 'Disposed')
    )
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, default=COND_FUNCT)
    
    # Availability
    AVAIL_UNLIMITED = 'UNLIMITED'
    AVAIL_LIMITED = 'LIMITED'
    AVAIL_UNAVAILABLE = 'UNAVAILABLE'
    AVAILABILITY_CHOICES = (
        (AVAIL_UNLIMITED, 'Unlimited'),
        (AVAIL_LIMITED, 'Limited'),
        (AVAIL_UNAVAILABLE, 'Unavailable')
    )
    availability = models.CharField(max_length=100, choices=AVAILABILITY_CHOICES, default=AVAIL_UNLIMITED)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    
    # Usage
    USAGE_YES = 'YES'
    USAGE_NO = 'NO'
    USAGE_ASK = 'ASK'
    USAGE_WITHINSPACE = 'WITHINSPACE'
    USAGE_CHOICES = (
        (USAGE_YES, 'OK for everybody'),
        (USAGE_NO, 'Don\'t even think about it...'),
        (USAGE_ASK, 'Ask'),
        (USAGE_WITHINSPACE, 'Within the Hackerspace')
    )
    usage_appropriate = models.CharField(max_length=255, choices=USAGE_CHOICES, default=USAGE_YES)
    usage_inappropriate = models.CharField(max_length=255, choices=USAGE_CHOICES, default=USAGE_ASK)
    usage_investigate = models.CharField(max_length=255, choices=USAGE_CHOICES, default=USAGE_ASK)
    usage_alter = models.CharField(max_length=255, choices=USAGE_CHOICES, default=USAGE_ASK)
    usage_takeaway = models.CharField(max_length=255, choices=USAGE_CHOICES, default=USAGE_NO)
    usage_exploit = models.CharField(max_length=255, choices=USAGE_CHOICES, default=USAGE_NO)
   
    usage_terms = models.TextField(blank=True)
    
    mounted = models.BooleanField()
    
    location_hint = models.CharField(max_length=255, blank=True)
    
    description = models.TextField(blank=True)

    # TODO Remove in future, when "labels" app is created ...
    label_created = models.DateTimeField(blank=True, editable=False, null=True)

    def get_absolute_url(self):
        return reverse('items:inventory_show', args=[str(self.uuid)])

    def __unicode__(self):
        return self.unique_name

    def has_change_permission(self, user):
        return self.inventoryownershipresponsibility_set.filter(person=user).exists()

    def is_owner(self, user):
        return self.inventoryownershipresponsibility_set.filter(person=user, is_owner=True).exists()

    def has_delete_permission(self, user):
        return self.is_owner(user)

    def get_location_path_photos(self):
        locations = self.location.get_ancestors(include_self=True)

        photos = []
        for location in locations:
            photos.extend(location.locationphoto_set.all())
        return photos


class InventoryPhoto(ImageModel):
    inventory = models.ForeignKey(Inventory)
    title = models.CharField(_('title'),
                             max_length=50,
                             blank=True)
    caption = models.TextField(_('caption'),
                               blank=True)
    date_added = models.DateTimeField(_('date added'),
                                      default=now)

    def __unicode__(self):
        if not self.title:
            return unicode(self.image)
        else:
            return self.title


class Person(auth.models.AbstractUser):
    nickname = models.CharField('Nickname',  max_length=255, help_text='ex: Miezekatze')
    street = models.CharField('Street', help_text=u'ex: Heilmannstra&szlig;e 30', max_length=255, blank=True)
    address_extra_mid = models.CharField('Address Extra Mid', help_text='ex: c/o the best of the best, sir',
                                         max_length=255, blank=True)
    zip_code = models.CharField('Zip Code', help_text='ex: 82049', max_length=255, blank=True)
    city = models.CharField('City', help_text='ex: Pullach', max_length=255, blank=True)
    state = models.CharField('State', help_text='ex: Oberbayern', max_length=255, blank=True)
    country = models.CharField('Country', help_text='ex: Germany', max_length=255, blank=True)
    address_extra_bot = models.CharField('Address Extra Bottom',  help_text='ex: aint no kiddin',
                                         max_length=255, blank=True)
    info = models.CharField('Info', help_text='ex: Miep Miep', max_length=255, blank=True)
    irc = models.CharField('IRC',  help_text='ex: #cccac@irc.hackint.eu', max_length=255, blank=True)
    jabber = models.CharField('Jabber', help_text='ex: miezekatze@jabber.ccc.de', max_length=255, blank=True)
    phone = models.CharField('Phone', help_text='ex: 0049 1234 677899', max_length=255, blank=True)
    wiki = models.CharField('Wiki', help_text='ex: URL to ur spaces wiki account/main page', max_length=255, blank=True)

    def get_absolute_url(self):
        return reverse('items:person_show', args=[str(self.id)])

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_staff:
            return True

        return super(auth.models.AbstractUser, self).has_module_perms(app_label)


class InventoryOwnershipResponsibility(models.Model):
    person = models.ForeignKey(Person)
    inventory = models.ForeignKey(Inventory)
    is_owner = models.BooleanField()

    class Meta:
        unique_together = (("person", "inventory"),)

    def __unicode__(self):
        return u'%s - %s' % (self.person, self.inventory)


# def slugify_attr_name(name):
#     return slugify(name.replace('_', '-')).replace('-', '_')

# class InventoryTypeKey(models.Model):
#     """
#     
#     """
#     TYPE_TEXT    = 'text'
#     TYPE_FLOAT   = 'float'
#     TYPE_DATE    = 'date'
#     TYPE_BOOLEAN = 'bool'
#     TYPE_ONE     = 'one'
#     TYPE_MANY    = 'many'
#     TYPE_RANGE   = 'range'
# 
#     DATATYPE_CHOICES = (
#         (TYPE_TEXT,    _('text')),
#         (TYPE_FLOAT,   _('number')),
#         (TYPE_DATE,    _('date')),
#         (TYPE_BOOLEAN, _('boolean')),
#         (TYPE_ONE,     _('choice')),
#         (TYPE_MANY,    _('multiple choices')),
#         (TYPE_RANGE,   _('numeric range')),
#     )
# 
#     type = models.ForeignKey(InventoryType)
#     title    =  models.CharField(_('title'), max_length=250, help_text=_('user-friendly attribute name'))
#     name     =  AutoSlugField(_('name'), max_length=250, populate_from='title',
#                              editable=True, blank=True, slugify=slugify_attr_name)
#     datatype =  models.CharField(_('data type'), max_length=5, choices=DATATYPE_CHOICES)
#     unit = models.CharField(max_length=255, blank = True)
#     help_text =  models.CharField(_('help text'), max_length=250, blank=True,
#                 help_text=_('short description for administrator'))
#     
#     searched =  models.BooleanField(_('include in search'))  # i.e. full-text search? mb for text only
#     filtered =  models.BooleanField(_('include in filters'))
#     sortable =  models.BooleanField(_('allow sorting'))
#     
#     def __unicode__(self):
#         return u'{0} - {1}'.format(self.type.name,self.name)
    
# class InventoryTypeValue(models.Model):
#     key = models.ForeignKey(InventoryTypeKey)
#     ab_inventory = models.ForeignKey(AbstractInventory)
#     value = models.CharField(max_length=255)
#     
#     class Meta:
#         unique_together = (('key', 'ab_inventory'))
#     
#     def __unicode__(self):
#         return u'{0} {1}({2}) : {3}'.format(self.unique_name,self.key.name,self.key.datatype, self.value)
