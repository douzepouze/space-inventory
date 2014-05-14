from django.conf.urls import patterns, url
from items import views

UUID_REGEXP = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = patterns(
    'items.views',
    url(r'^$', views.inventory_list, name='inventory_list'),
    url(r'^inventory/(?P<req_uuid>' + UUID_REGEXP + ')/?$', views.inventory_show, name='inventory_show'),
    url(r'^location/(?P<req_uuid>' + UUID_REGEXP + ')/?$', 'location_show', name='location_show'),
    url(r'^type/(?P<id>\d+)/?$', 'inventory_type_show', name='inventory_type_show'),
    url(r'^person/(?P<id>\d+)/?$', 'person_show', name='person_show'),
)