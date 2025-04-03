from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'github',
       'USER': 'postgres',
       'PASSWORD': 'nimai1234$',
       'HOST': 'localhost',
       'PORT': '5432',
   }
}



