from django.conf import settings

def inventory(request):
    return {
        'inventory_name':"CCCAC Inventory",
        'DEBUG': settings.DEBUG
    }