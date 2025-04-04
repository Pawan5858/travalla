from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'railway',
       'USER': 'postgres',
       'PASSWORD': 'bGfSbpiBxjQHduVdTfgHSzlQDLiAmYlk$',
       'HOST': 'postgres.railway.internal',
       'PORT': '5432',
   }
}
