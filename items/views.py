# Python Imports
import base64
import urllib
import uuid

# Django Imports
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count

from django.http.response import Http404
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.utils.html import escape
from items.forms import InventoryImageUploadForm, LocationImageUploadForm
# from bootstrap_toolkit.widgets import BootstrapUneditableInput

# from .forms import TestForm, TestModelForm, TestInlineForm, WidgetsForm, FormSetInlineForm

# Local Imports
from items.models import Inventory, InventoryPhoto, Location, InventoryType


def make_tree(objects):
    result = []
    nesting = [(None, iter(objects))]
    while len(nesting):
        try:
            l = next(nesting[-1][1])
        except:
            nesting.pop()
            continue
        if l.parent != nesting[-1][0]:
            continue
        # this is a workaround for the inability to repeat something in the templates
        l.depth_prefix = "&nbsp;" * (2 * (len(nesting) - 1))
        l.found_children = []
        result.append(l)
        for p in nesting[1:]:
            p[0].found_children.append(l.id)
        nesting.append((l, iter(objects)))
    return result


def inventory_list(request):
    epp_list = [15, 25, 40, 50, 100]

    # make a tree from locations and types
    locations = make_tree(Location.objects.all())
    types = make_tree(InventoryType.objects.all())

    # construct a dict of filters
    filters = {}
    person_kind = int(request.GET.get("person_kind", 3))
    person_name = request.GET.get("person_name", "")

    if person_name:
        filters["inventoryownershipresponsibility__person__username__iexact"] = person_name
        if person_kind != 3:
            filters["inventoryownershipresponsibility__is_owner"] = person_kind & 2
    text = request.REQUEST.get("text", "")
    image_filter = request.REQUEST.get("image_filter", "")

    search = {"person_name": person_name, "person_kind": person_kind, "text": text, "image_filter": image_filter}

    for i in ("location", "type"):
        exact = search[i + '_exact'] = int(request.GET.get(i + "_exact", 0))
        search[i] = choice = int(request.GET.get(i, -1))
        if choice >= 0:
            if exact:
                filters[i + "_id"] = choice
            else:
                for j in locals()[i + "s"]:
                    if j.id == choice:
                        filters[i + "_id__in"] = j.found_children + [j.id]
    search["params"] = "&" + urllib.urlencode(search)
    filters = Q(**filters)
    if text != "":
        filters &= reduce(
            lambda q, v: q | Q(**{("%s__icontains" % v): text}),
            ("unique_name",
             "manufacturer",
             "name",
             "serial",
             "usage_terms",
             "location_hint",
             "description"),
            Q())

    if image_filter == "onlywith":
        filters &= Q(inventoryphoto__count__gt=0)
    elif image_filter == "onlywithout":
        filters &= Q(inventoryphoto__count=0)
    else:
        search['image_filter'] = "none"

    objects = Inventory.objects.annotate(Count("inventoryphoto")).filter(filters).order_by("-id")

    # check new elements per page is set
    if 'epp' in request.GET:
        request.session['epp'] = int(request.GET.get('epp', epp_list[0]))

    paginator = Paginator(objects, int(request.session.get('epp', epp_list[0])))
    page = request.GET.get('page')
    try:
        paged_inv = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_inv = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_inv = paginator.page(paginator.num_pages)

    return render_to_response('inventory_list.html', RequestContext(request, {
        'inventorys': paged_inv,
        'locations': locations,
        'types': types,
        'search': search,
        'epp': int(request.session.get('epp', epp_list[0])),
        'epp_list': epp_list
    }))


def inventory_show(request, req_uuid):
    try:
        inventory = Inventory.objects.get(uuid=req_uuid)
    except Inventory.DoesNotExist:
        raise Http404

    image_upload_factory = formset_factory(InventoryImageUploadForm, extra=1)

    if request.method == 'POST':
        formset = image_upload_factory(request.POST, request.FILES)  # bound formset
        if formset.is_valid():
            if request.user.is_authenticated():
                for form in formset:
                    image = form.save(commit=False)
                    if bool(image.image):
                        image.inventory = inventory
                        image.save()
                        formset = image_upload_factory()  # Unbound formset
            else:
                messages.error(request, 'Only authenticated users are able to add photos.')
    else:
        formset = image_upload_factory()  # Unbound formset

    return render_to_response('inventory_detail.html', RequestContext(request, {
        'inventory': inventory,
        'formset': formset
    }))


def dispatch_encoded_uuids(request, encoded_uuid):
    try:
        uuid_decoded = str(uuid.UUID(bytes=base64.urlsafe_b64decode(str(encoded_uuid + '='*(3 & -len(encoded_uuid))))))

        for ct in ContentType.objects.filter(app_label="items"):
            try:
                obj = ct.get_object_for_this_type(uuid=uuid_decoded)
                return redirect(obj)
            except (ObjectDoesNotExist, FieldError):
                pass
        raise ObjectDoesNotExist

    except ValueError:
        messages.error(request, u'Malformed encoded uuid "%s".' % (escape(encoded_uuid), ))
    except ObjectDoesNotExist:
        messages.error(request, u'Object with uuid "%s" not found.' % (escape(uuid_decoded), ))

    return redirect('start')


def location_show(request, req_uuid):
    try:
        location = Location.objects.get(uuid=req_uuid)
    except Location.DoesNotExist:
        raise Http404

    image_upload_factory = formset_factory(LocationImageUploadForm, extra=1)

    if request.method == 'POST':
        formset = image_upload_factory(request.POST, request.FILES)  # bound formset
        if formset.is_valid():
            if request.user.is_authenticated():
                for form in formset:
                    image = form.save(commit=False)
                    if bool(image.image):
                        image.location = location
                        image.save()
                        formset = image_upload_factory()  # Unbound formset
            else:
                messages.error(request, 'Only authenticated users are able to add photos.')
    else:
        formset = image_upload_factory()  # Unbound formset
    
    return render_to_response('location_detail.html', RequestContext(request, {
        'location': location,
        'formset': formset,
    }))


def person_show(request, id):
    pass


def inventory_type_show(request, id):
    pass


def demo_form_with_template(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = TestForm(request.POST)
        form.is_valid()
    else:
        form = TestForm()
    modelform = TestModelForm()
    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


def demo_form_inline(request):
    layout = request.GET.get('layout', '')
    if layout != 'search':
        layout = 'inline'
    form = TestInlineForm()
    return render_to_response('form_inline.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


def demo_formset(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'inline'
    DemoFormSet = formset_factory(FormSetInlineForm)
    if request.method == 'POST':
        formset = DemoFormSet(request.POST, request.FILES)
        formset.is_valid()
    else:
        formset = DemoFormSet()
    return render_to_response('formset.html', RequestContext(request, {
        'formset': formset,
        'layout': layout,
    }))


def demo_tabs(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'tabs'
    tabs = [
        {
            'link': "#",
            'title': 'Tab 1',
            },
        {
            'link': "#",
            'title': 'Tab 2',
            }
    ]
    return render_to_response('tabs.html', RequestContext(request, {
        'tabs': tabs,
        'layout': layout,
    }))


def demo_widgets(request):
    layout = request.GET.get('layout', 'vertical')
    form = WidgetsForm()
    return render_to_response('form.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))
