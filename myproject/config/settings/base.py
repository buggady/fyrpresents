"""
Django settings for fyrpresents project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys, os
from unipath import Path
from secrets import *

from oscar.defaults import *

#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = Path(__file__).ancestor(3)

ALLOWED_HOSTS = ['texasfyre.com','fyrpresents.com', '127.0.0.1', '74.220.216.114']

ADMINS = (('Nick', 'nicolasdeshefy@gmail.com'),)
SERVER_EMAIL = 'info@fyrpresents.com'

from oscar import get_core_apps
INSTALLED_APPS = [
    'fyrpresents',
    'events',
    'users',
    'mingle',
    'market',
    'mathfilters',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'facebook_sdk',
    'newsletter',
    'django_premailer',
    'django_extensions',
    'djstripe',
    'vote',
    'photologue',
    'sortedm2m',
    'taggit',
    'compressor',
    'widget_tweaks',
    'django_comments_xtd',
    'django_comments',
    'mptt',
    'tagging',
    'zinnia',
    'schedule',
    'address',
    'annoying',
    'endless_pagination',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu', 
    'admin_tools.dashboard',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + get_core_apps()

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]
    
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.child("templates"),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
		        'django.core.context_processors.i18n',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Details Secret

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR.parent.child("static")
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR.parent.child("media")
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 2

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 1

LOGIN_URL='/accounts/login/'
LOGIN_REDIRECT_URL='/register/'
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
SOCIALACCOUNT_QUERY_EMAIL = True

CRISPY_TEMPLATE_PACK='bootstrap3'

EMAIL_BACKEND = 'django_sendmail_backend.backends.EmailBackend'
EMAIL_USE_SSL = True
#Email Details Secret
DEFAULT_FROM_EMAIL = 'info@fyrpresents.com'
EMAIL_PORT = 465

DJSTRIPE_INVOICE_FROM_EMAIL="accounts@fyrpresents.com"

NEWSLETTER_CONFIRM_EMAIL = False

PHOTOLOGUE_GALLERY_SAMPLE_SIZE=10

COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 2
COMMENTS_XTD_CONFIRM_EMAIL = True

ADMIN_TOOLS_MENU = 'myproject.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'myproject.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'myproject.dashboard.CustomAppIndexDashboard'
ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

OSCAR_SHOP_NAME = "The Rave Trade"
OSCAR_SHOP_TAGLINE = "Share your art, check out other's art!"