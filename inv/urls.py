# Django Imports
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from items.urls import UUID_REGEXP
import items.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'inv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #url('^markdown/', include('django_markdown.urls')),

    url(r'^$', 'items.views.inventory_list', name="start"),
    url(r'^A/(?P<encoded_uuid>[a-zA-Z0-9_-]+)/?$', items.views.dispatch_encoded_uuids, name='dispatch_encoded_uuids'),
    url(r'^items/', include('items.urls', 'items')),
    url(r'^photologue/', include('photologue.urls')),
# Will only work on development serving via manage.py runserver
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )