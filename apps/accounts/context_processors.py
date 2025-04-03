# apps/admin_user/context_processors.py
from django.conf import settings

def recaptcha_context(request):
    print("===================================", settings.RECAPTCHA_SITE_KEY)
    print("===================================", settings.RECAPTCHA_SITE_KEY)
    print("===================================", settings.RECAPTCHA_SITE_KEY)
    return {
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY
    }