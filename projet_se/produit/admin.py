from django.contrib import admin
from .models import Produit

try:
    admin.site.unregister(Produit)
except admin.sites.NotRegistered:
    pass

admin.site.register(Produit)
