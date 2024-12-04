from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

# # Check if User model is already registered before registering it
# if not admin.site.is_registered(User):
#     admin.site.register(User)

# Vérifier si le modèle User est déjà enregistré avant de l'enregistrer
if User not in admin.site._registry:
    @admin.register(User)
    class UserAdmin(admin.ModelAdmin):
        list_display = ('first_name', 'last_name', 'email')
        search_fields = ['email', 'first_name', 'last_name']
