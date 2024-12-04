from django.contrib import admin
from .models import Evaluation
from users.models import User
from produit.models import Produit


admin.site.register(Evaluation)
admin.site.register(Produit)
admin.site.register(User)