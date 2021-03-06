"""
Django settings for herbario1 project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$&a7azey)pqip%@dbgw6=9m)eeow_ls^l6wb4eac1)c4l)p%_&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'snowpenguin.django.recaptcha2',
    'categoriaTaxonomica',
    'cientifico',
    'coleccion',
    'especimen',
    'ubicacion',
    'usuario',
    'noticia',
    'visita',
    'cliente',
    'servicios',
    'prestamo',
    'cargarArchivo',
    'easy_thumbnails',  # para permitir que aparezca imagen en el formulario de especimen
    'crispy_forms',  # para permitir que aparezca imagen ene l formulario de especimen
    'bootstrap3',  # permite tags de boostrap
    'rolepermissions',  # librerias para el manejo de permisos
    # 'channels', #webservices


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'herbario1.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'herbario1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


""" DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  
        'NAME': 'abodsovk',  
        'USER': 'abodsovk',  
        'PASSWORD': 'LXUfCnIKGTHOuE8UqUj4s80eYGJZ49X1',  
        'HOST': 'hard-plum.db.elephantsql.com',  
        'PORT': '5432',  
    }  
} """

# DATABASES = {
#       'default': {
#           'ENGINE': 'django.db.backends.sqlite3',
#           'NAME': 'mydatabase',
#       }
#       }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'herbario',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticbase'), ]
# para el manejo de las imagenes
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# permite enviar mensajes de alerta al usuario
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# redirecciona a la pantalla de principal en caso que un usuario queira acceder a una url portegida sin estar logueado
LOGIN_URL = '/'

# para el envio de mensajes
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'angiepmc93@gmail.com'
EMAIL_HOST_PASSWORD = 'A.P.Medina-1208'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'Herbario CUVC  <noreply@example.com>'

# reconozca el archivo roles.py
ROLEPERMISSIONS_MODULE = 'herbario1.roles'
ROLEPERMISSIONS_REDIRECT_TO_LOGIN = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 5 * 60  # 5 minutes


RECAPTCHA_PUB_KEY = "6Ld6VegUAAAAAFzxQb8rka9FQWAdVCZDQTbsrP30"
GOOGLE_RECAPTCHA_SECRET_KEY = "6Ld6VegUAAAAAAKPhtPOyQLiBEC_IyU6RWWhYF98"