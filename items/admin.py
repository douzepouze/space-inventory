# -*- coding: utf-8 -*-

import base64
import textwrap

# Django Imports
from django.contrib import admin
# from django.contrib.admin.helpers import Fieldset
from django import forms
from django.shortcuts import render
from django.contrib.admin import helpers
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
# from django.conf import settings
# from django.http import HttpResponse
from django.conf.urls import patterns, url
# from django.shortcuts import render_to_response
# from django.template.context import RequestContext
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

# 3rd Party
# to generate the pdf and response in our custom view
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
# from django_markdown.admin import MarkdownModelAdmin
from mptt.admin import MPTTModelAdmin


# Local
from items.models import *
from forms import PersonCreationForm


def generate_qr_codes(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("generate_qr_code_report/setup/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

generate_qr_codes.short_description = "Generate QR Codes for the selected items"


class InventoryOwnershipResponsibilityInline(admin.TabularInline):
    model = InventoryOwnershipResponsibility
    extra = 1
    # TODO funktioniert nicht, kA warum.
    # def has_change_permission(self, request, obj=None):
    #     if super(InventoryOwnershipResponsibilityInline, self).has_change_permission(request):
    #         return True
    #
    #     # Check whether the User owns some resp. a specific obj
    #     if obj is None:
    #         if InventoryOwnershipResponsibility.objects.filter(person=request.user, is_owner=True).exists():
    #             return True
    #         else:
    #             return False
    #     else:
    #         return obj.is_owner(request.user)

    # def has_delete_permission(self, request, obj=None):
    #     if super(InventoryOwnershipResponsibilityInline, self).has_delete_permission(request):
    #         return True
    #
    #     # Check whether the User owns some resp. a specific obj
    #     if obj is None:
    #         if InventoryOwnershipResponsibility.objects.filter(person=request.user, is_owner=True).exists():
    #             return True
    #         else:
    #             return False
    #     else:
    #         return obj.is_owner(request.user)


    # def get_queryset(self, request):
    #     """
    #     Narrows Inventory List down to owned items in case the user is not a superuser.
    #     @param request:
    #     @return:
    #     """
    #     qs = super(InventoryOwnershipResponsibilityInline, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(inventoryownershipresponsibility__person=request.user)


class InventoryRelatedItems(admin.TabularInline):
    model = Inventory.related_items.through
    fk_name = "to_inventory"
    extra = 1


class InventoryPhotoInline(admin.TabularInline):
    model = InventoryPhoto
    fk_name = 'inventory'
    extra = 1


class LabelPaper(object):
    margin = (0, 0, 0, 0)  # north east south west
    dimension = (0, 0)  # label dimension
    grid = (0, 0)  # columns/rows
    labels_per_sheet = 0
    offset = 0  # label offset number - when #offset labels are already printed in the first shee

    def __init__(self, offset):
        self.offset = offset
        self.labels_per_sheet = self.grid[0]*self.grid[1]


class SmallPaper(LabelPaper):
    margin = (6, 5, 6, 5)
    dimension = (18, 18)
    grid = (10, 15)

    def __init__(self, offset):
        self.coords = [(x, y) for y in range(self.margin[0], 15*18+9, 18) for x in range(self.margin[1], 10*18+14, 18)]
        super(SmallPaper, self).__init__(offset)

    def draw_labels(self, p, index, item, ct):
        pos = self.coords[index]
        qrw = QrCodeWidget(settings.LABEL_DISPATCHER_URL + base64.urlsafe_b64encode(uuid.UUID(item.uuid).bytes).rstrip('='),
                           barBorder=0, barWidth=16*mm, barHeight=16*mm)
        width, height = A4
        d = Drawing(32, 32)
        d.add(qrw)
        renderPDF.draw(d, p, pos[0]*mm+2*mm, height-pos[1]*mm+1*mm-self.dimension[1]*mm)


class MediumPaper(LabelPaper):
    margin = (14, 0, 14, 0)
    dimension = (70, 20)
    grid = (3, 14)

    def __init__(self, offset):
        self.coords = [(x, y) for y in range(self.margin[0], self.grid[1]*self.dimension[1], self.dimension[1]) for x in range(self.margin[1], self.grid[0]*self.dimension[0], self.dimension[0])]
        super(MediumPaper, self).__init__(offset)

    def draw_labels(self, p, index, item, ct):
        pos = self.coords[index]
        qrw = QrCodeWidget(settings.LABEL_DISPATCHER_URL + base64.urlsafe_b64encode(uuid.UUID(item.uuid).bytes).rstrip('='),
                           barBorder=0, barWidth=12*mm, barHeight=12*mm)
        width, height = A4
        corrected_height = height-pos[1]*mm+1*mm-self.dimension[1]*mm
        d = Drawing(self.dimension[0]*mm, self.dimension[1]*mm)
        d.add(qrw)

        # unique name

        # type/location/besitzer
        textobject = p.beginText()
        textobject.setTextOrigin(pos[0]*mm+17*mm, corrected_height+self.dimension[1]*mm-9)
        textobject.setFont("Helvetica", 9)
        if ct == 11:
            text = u'%s Type: %s; Loc: %s; Pers: %s' % (item.unique_name,
            u' -> '.join([unicode(x) for x in item.type.get_ancestors(include_self=True)]),
            u' -> '.join([unicode(x) for x in item.location.get_ancestors(include_self=True)]),
            u', '.join([unicode(x.nickname) for x in item.persons.all()]))
        elif ct == 8:
            text = u'%s; %s; In: %s' % (item.name,
            item.description_short,
            u' -> '.join([unicode(x) for x in item.get_ancestors()]))
        else:
            pass
        textobject.textLines(textwrap.wrap(text, 30))
        p.drawText(textobject)

        # p.rect(pos[0]*mm, corrected_height, self.dimension[0]*mm, self.dimension[1]*mm, fill=0, stroke=1)
        renderPDF.draw(d, p, pos[0]*mm+4*mm, corrected_height+6*mm)


class InventoryAdmin(admin.ModelAdmin):
    label_template = 'admin/items/labels_choose_format.html'
    inlines = (InventoryOwnershipResponsibilityInline, InventoryPhotoInline)
    list_display = ('__unicode__', 'uuid', 'serial', 'condition', 'availability')
    list_filter = ('condition', 'availability')
    # exclude = ('related_items', )
    actions = [generate_qr_codes]
    fieldsets = [
        (None,
         {'fields':
          ['unique_name',
           'name',
           'manufacturer',
           'consumable',
           'movable',
           'mounted',
           'serial',
           'location',
           'type',
           'location_hint',
           'condition',
           'availability'
           ]
          }
         ),
        ('Availability Information',
         {'fields':
          ['available_from',
           'available_to'
           ], 'classes': ['collapse']
          }
         ),
        ('Usage Terms',
         {'fields':
          ['usage_appropriate',
           'usage_inappropriate',
           'usage_investigate',
           'usage_alter',
           'usage_takeaway',
           'usage_exploit',
           'usage_terms',
           ]  # , 'classes': ['collapse']
          }
         ),
        ('Related Items',
         {'fields':
          ['related_items',
           ]  # , 'classes': ['collapse']
          }
         ),
        ('Item Description (Markdown support)',
         {'fields':
          ['description']
          })
    ]

    def get_urls(self):
        """ 
        Override to add our custom report view.
        """
        urls = super(InventoryAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^generate_qr_code_report/(?P<step>(setup|print|evaluate))/$',
                self.admin_site.admin_view(self.generate_qr_code_report),
                name='items_inventory_generate_qr_code_report')
        )
        return my_urls + urls

    class LabelSetupForm(forms.Form):
        # Location Types
        TYPE_CHOICES = (
            ('small', 'Kleine Label - Nur QR-Code'),
            ('medium', 'QR-Code+Name+Short Desc.'),
            ('large', 'QR-Code+Desc+Usage-Terms')
        )
        label_papers = {'small': SmallPaper, 'medium': MediumPaper, 'large': None}

        type = forms.ChoiceField(label='Paper Type', choices=TYPE_CHOICES)
        offset = forms.IntegerField(label='Start Offset')

    def generate_qr_code_report(self, request, step=None):
        if step is None or step == 'setup':
            context = {
                'title': 'Inventory Label Format',
                'app_label': self.model._meta.app_label,
                'has_change_permission': self.has_change_permission(request),
                'ct': request.GET['ct'],
                'ids': request.GET['ids'],
                'opts': self.model._meta
            }

            # Handle form request
            if request.method == 'POST':
                form = self.LabelSetupForm(request.POST, request.FILES)
                if form.is_valid():
                    # Create the HttpResponse object with the appropriate PDF headers.
                    response = HttpResponse(mimetype='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="labels.pdf"'

                    p = canvas.Canvas(response)

                    model = ContentType.objects.get_for_id(request.GET['ct']).model_class()
                    selected_ids = request.GET['ids'].split(',')

                    paper = self.LabelSetupForm.label_papers[request.POST['type']](request.POST['offset'])

                    i = int(request.POST['offset'])
                    for item in model.objects.filter(id__in=selected_ids):
                        paper.draw_labels(p, i, item, int(request.GET['ct']))
                        i += 1

                    p.showPage()
                    p.save()
                    return response
            else:
                form = self.LabelSetupForm(initial={'offset': 0})
            context['form'] = form

            context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                                     self.get_prepopulated_fields(request))

            return render(request, self.label_template, context)
        elif step == 'evaluate':
            pass


#         model = ContentType.objects.get_for_id(request.GET['ct']).model_class()
#         selectedIDs = request.GET['ids'].split(',')
#
#         # Create the HttpResponse object with the appropriate PDF headers.
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename="qr_codes.pdf"'
#
#         pdf = FPDF(format='A4')
#         pdf.compress = False
#         pdf.set_margins(left=0,right=0,top=0)
#         pdf.add_page()
#         pdf.set_font('helvetica', '', 13.0)
#
#  #       i = 1
# #        for item in model.objects.filter(id__in=selectedIDs):
#         for pos in [(x,y) for x in range(32,10*18+14,18) for y in range(26,15*18+9,18)]:
#             pdf.set_xy(pos[0],pos[1])
#             #pdf.cell(ln=0, h=18.0, w=18.0, align='C',  txt='', border=0)
#             pdf.set_xy(pos[0], pos[1])
#
#             qr = qrcode.QRCode(
#                 version=1,
#                 error_correction=qrcode.constants.ERROR_CORRECT_L,
#                 box_size=10,
#                 border=0,
#             )
#             qr.add_data('http://aachen.ccc.de')
#             qr.make(fit=True)
#
#             img = qr.make_image()
#
#             pdf.image(img, pos[0]+1, pos[1]+1, type='PIL', w=16, h=16)
#             #i = i + 1
#
#         content = pdf.output(dest='S')
#         response.write(content)
#
#         return response

    # def has_change_permission(self, request, obj=None):
    #     if super(InventoryAdmin, self).has_change_permission(request):
    #         return True
    #
    #     # Check whether the User is responsible for some resp. a specific obj
    #     if obj is None:
    #         if InventoryOwnershipResponsibility.objects.filter(person=request.user).exists():
    #             return True
    #         else:
    #             return False
    #     else:
    #         return obj.has_change_permission(request.user)
    #
    # def has_delete_permission(self, request, obj=None):
    #     if super(InventoryAdmin, self).has_delete_permission(request):
    #         return True
    #
    #     # Check whether the User owns some resp. a specific obj
    #     if obj is None:
    #         if InventoryOwnershipResponsibility.objects.filter(person=request.user, is_owner=True).exists():
    #             return True
    #         else:
    #             return False
    #     else:
    #         return obj.has_delete_permission(request.user)
    #
    # def get_queryset(self, request):
    #     """
    #     Narrows Inventory List down to owned items in case the user is not a superuser.
    #     @param request:
    #     @return:
    #     """
    #     qs = super(InventoryAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(inventoryownershipresponsibility__person=request.user)


class InventoryPhotoAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'title',  'admin_thumbnail']


class LocationPhotoAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'title', 'admin_thumbnail']


class PersonAdmin(UserAdmin):
    add_form = PersonCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name',
                                         'last_name',
                                         'email',
                                         'nickname',
                                         'street',
                                         'address_extra_mid',
                                         'zip_code',
                                         'city',
                                         'state',
                                         'country',
                                         'address_extra_bot',
                                         'info',
                                         'irc',
                                         'jabber',
                                         'phone',
                                         'wiki')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class LocationAdmin(MPTTModelAdmin):
    label_template = 'admin/items/labels_choose_format.html'
    actions = [generate_qr_codes]

    class LabelSetupForm(forms.Form):
        # Location Types
        TYPE_CHOICES = (
            ('small', 'Kleine Label - Nur QR-Code'),
            ('medium', 'QR-Code+Name+Short Desc.'),
            ('large', 'QR-Code+Desc+Usage-Terms')
        )
        label_papers = {'small': SmallPaper, 'medium': MediumPaper, 'large': None}

        type = forms.ChoiceField(label='Paper Type', choices=TYPE_CHOICES)
        offset = forms.IntegerField(label='Start Offset')

    def generate_qr_code_report(self, request, step=None):
        if step is None or step == 'setup':
            context = {
                'title': 'Inventory Label Format',
                'app_label': self.model._meta.app_label,
                'has_change_permission': self.has_change_permission(request),
                'ct': request.GET['ct'],
                'ids': request.GET['ids'],
                'opts': self.model._meta
            }

            # Handle form request
            if request.method == 'POST':
                form = self.LabelSetupForm(request.POST, request.FILES)
                if form.is_valid():
                    # Create the HttpResponse object with the appropriate PDF headers.
                    response = HttpResponse(mimetype='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="labels.pdf"'

                    p = canvas.Canvas(response)

                    model = ContentType.objects.get_for_id(request.GET['ct']).model_class()
                    selected_ids = request.GET['ids'].split(',')

                    paper = self.LabelSetupForm.label_papers[request.POST['type']](request.POST['offset'])

                    i = int(request.POST['offset'])
                    for item in model.objects.filter(id__in=selected_ids):
                        paper.draw_labels(p, i, item, int(request.GET['ct']))
                        i += 1

                    p.showPage()
                    p.save()
                    return response
            else:
                form = self.LabelSetupForm(initial={'offset': 0})
            context['form'] = form

            context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                                     self.get_prepopulated_fields(request))

            return render(request, self.label_template, context)
        elif step == 'evaluate':
            pass

    def get_urls(self):
        """
        Override to add our custom report view.
        """
        urls = super(LocationAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^generate_qr_code_report/(?P<step>(setup|print|evaluate))/$',
                self.admin_site.admin_view(self.generate_qr_code_report),
                name='items_location_generate_qr_code_report')
        )
        return my_urls + urls

admin.site.register(Location, LocationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(InventoryType, MPTTModelAdmin)
admin.site.register(InventoryPhoto, InventoryPhotoAdmin)
admin.site.register(LocationPhoto, LocationPhotoAdmin)