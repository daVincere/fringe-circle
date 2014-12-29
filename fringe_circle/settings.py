"""
Django settings for fringe_circle project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kgob1q3=*&9o!0&km#ai&4lx6m)&j@-9^1hu*27%!%@3u(288$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#uploading path for media files
MEDIA_ROOT=os.path.join(BASE_DIR,"fringe_x","static")


TEMPLATE_DEBUG = True
TEMPLATE_DIRS=(os.path.join(BASE_DIR,"media"),
)

STATICFILES_DIRS=(os.path.join(BASE_DIR,"media"),)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fringe_x',
    'fringe_discussion',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fringe_circle.urls'

WSGI_APPLICATION = 'fringe_circle.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fringe_circle_db',
        'USER':'postgres',
        'PASSWORD':'Goodguysimon13130#',
        'PORT':'5432',
        'HOST':'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# multiuploader settings
MULTIUPLOADER_FILES_FOLDER=os.path.join(BASE_DIR,'fringe_x','static','product_images')

MULTIUPLOADER_FILE_EXPIRATION_TIME=3600

MULTIUPLOADER_FORMS_SETTINGS={
    'default':{
        'FILE_TYPES':["jpg","jpeg","png"],
        'CONTENT_TYPES':['image/jpeg','image/png'],
        'MAX_FILE_SIZE':2097152,
        'MAX_FILE_NUMBER':8,
        'AUTO_UPLOAD':True,
    },

}