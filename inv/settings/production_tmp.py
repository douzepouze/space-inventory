from inv.settings.base import *


SECRET_KEY = '...'
DEBUG = False
TEMPLATE_DEBUG = False

BASE_DIR = "..."
ALLOWED_HOSTS = ["...."]
LABEL_DISPATCHER_URL = 'https://inv.ccc.ac/A/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}

MEDIA_ROOT = os.path.join('/', '...', 'media_root')

MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ('assets', os.path.join(BASE_DIR, '../../static')),
)

STATIC_URL = '/static/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATIC_ROOT = os.path.join('/', '...', 'static_root')