from pathlib import Path
import os
from django.contrib.messages import constants as messages

BASE_DIR=Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in ('1', 'true', 'yes', 'on')


SECRET_KEY=os.getenv('DJANGO_SECRET_KEY','django-insecure-change-me-for-local-development')
DEBUG=env_bool('DJANGO_DEBUG')
ALLOWED_HOSTS=[host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS','localhost,127.0.0.1,testserver').split(',') if host.strip()]
INSTALLED_APPS=[
    'covidtracker.apps.CovidtrackerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE=[
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF='thesis.urls'
TEMPLATES=[{
        'BACKEND':'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR,'templates')],
        'APP_DIRS':True,
        'OPTIONS':{
            'context_processors':[
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION='thesis.wsgi.application'
DATABASES={
    'default':{
        'ENGINE':'django.db.backends.sqlite3',
        'NAME':os.getenv('DJANGO_DATABASE_NAME',BASE_DIR/'db.sqlite3'),
    }
}
AUTH_PASSWORD_VALIDATORS=[{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },{
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },{
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_I18N=True
USE_TZ=True
STATIC_URL='/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
STATIC_ROOT=os.getenv('DJANGO_STATIC_ROOT',os.path.join(BASE_DIR,'assets'))
STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL='/images/'
MEDIA_ROOT=os.getenv('DJANGO_MEDIA_ROOT',os.path.join(BASE_DIR,'images'))
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
SECURE_SSL_REDIRECT=env_bool('DJANGO_SECURE_SSL_REDIRECT')
SECURE_HSTS_SECONDS=int(os.getenv('DJANGO_SECURE_HSTS_SECONDS','0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS=env_bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS')
SECURE_HSTS_PRELOAD=env_bool('DJANGO_SECURE_HSTS_PRELOAD')
SESSION_COOKIE_SECURE=env_bool('DJANGO_SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE=env_bool('DJANGO_CSRF_COOKIE_SECURE')
MESSAGE_TAGS={
    messages.ERROR:'danger',
}
