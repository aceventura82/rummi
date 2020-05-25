"""
server setup
sudo dnf install python-devel mod_wsgi mariadb-devel
sudo pip install virtualenv django uwsgi
If global install else instal in virtualenv
sudo pip install django_extensions django-translation-manager mysqlclient

Initial project setup
cd /var/www/django/
sudo virtualenv projectenv
. /var/www/django/projectenv/bin/activate
sudo pip install django_extensions django-translation-manager mysqlclient
python manage.py makemigration
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

NginX setup
sudo ln -s /var/data/python/django/rummi/rummi_uwsgi.ini /etc/uwsgi/vassals/
cp ../rummi/uwsgi_params .
. ../projectenv/bin/activate

Vhost Example --------------------
upstream django {
    server unix:///var/data/python/django/rummi/rummi.sock; # for a file socket
    # server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}
server{
    location /static {
        alias /var/data/python/django/rummi/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /var/data/python/django/rummi/uwsgi_params; # the uwsgi_params file you installed
    }
}
------------------------------------------------

Apache Vhost Example -------------
Alias /static /var/www/django/rummi/static
<Directory /var/www/django/rummi/static>
    Require all granted
</Directory>

<Directory /var/www/django/rummi/rummi>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>
WSGIDaemonProcess rummi python-path=/var/www/django/rummi:/var/www/django/projectenv/lib/python3.8/site-packages
WSGIProcessGroup rummi
WSGIScriptAlias / /var/www/django/rummi/rummi/wsgi.py
------------------------------------------------

sudo python manage.py runserver 0:80
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+#vef!#q_^*%a5c@1!e(dt^*8/500m#sw4ckcghci@bmmibnb&j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['rummi.servoz.tk', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rummiApp.apps.rummiAppConfig',
    'django_extensions',
    'translation_manager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'rummi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rummi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rummi',
        'HOST': '127.0.0.1',
        'USER': 'rummi_usr',
        'PASSWORD': '3x1Fkx6UtNM1ED7d)sZvo&Y0se%'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DJANGO_LOG_LEVEL = DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/rummiApp/logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'

LOCALE_PATHS = [
    BASE_DIR+'/locale/',
]
TRANSLATIONS_BASE_DIR = ''
TRANSLATIONS_PROJECT_BASE_DIR = BASE_DIR
TRANSLATIONS_SYNC_REMOTE_URL = ''


FROMEMAIL = 'no-reply@servoz.tk'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'no-reply@servoz.tk'
# EMAIL_HOST_PASSWORD = '$af4VAYU1ER-3%!'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'Rummi App <info@servoz.tk>'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
LOGIN_URL = '/login/'
LOGOUT_URL = '/'
ADMIN_URL = 'AdminRummi/'
LOGIN_REDIRECT_URL = '/'+ADMIN_URL
LANGUAGES = (('en', 'English'), ('es', 'Español'))
LOGPATH = BASE_DIR + 'rummiApp/logs/'

AUTH_PASSWORD_VALIDATORS = []
