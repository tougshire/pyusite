from django.conf import settings


def pyusite(request):
    return {"pyusite": settings.PYUSITE}
