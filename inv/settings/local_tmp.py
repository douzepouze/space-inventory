from inv.settings.base import *
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

DEBUG = True
TEMPLATE_DEBUG = True

# Application definition
THIRD_PARTY_APPS += (
    'debug_toolbar',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

from os.path import expanduser, isdir, join
home_tmp = join(expanduser("~"), 'tmp', 'inventory')

MEDIA_ROOT = join(home_tmp, 'media_root')
STATIC_ROOT = join(home_tmp, 'static_root')

if not isdir(MEDIA_ROOT):
    raise Exception('Directory for temporary media_root `%s` does not exist.' % (MEDIA_ROOT,))

if not isdir(STATIC_ROOT):
    raise Exception('Directory for temporary static_root `%s` does not exist.' % (STATIC_ROOT,))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(home_tmp, 'db.sqlite3'),
    }
}