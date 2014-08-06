import os
from adopt4k_server.settings.base import *


ALLOWED_HOSTS = []

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!*oi^_@brc#8+p7_8y_85mhpa)y0q7%j%-wwdq9ucwq0(7kc*%'

STATICFILES_DIRS = ( 
    os.path.join(BASE_DIR, "STATIC"), 
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'adoptdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}