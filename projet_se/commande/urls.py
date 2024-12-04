from django.urls import path
from . import views

urlpatterns = [
    path("", views.produitcommande_list, name='produitcommande_list'),
    path('add-to-commande/', views.click_button_add_to_commande, name='click_button_add_to_commande'),
path('delete_commande/<int:id>/', views.delete_commande, name='delete_commande'),
    path('edit_commande/<int:commande_id>/', views.edit_commande, name='edit_commande'),
    path('update-quantity/<int:commande_id>/', views.update_quantity, name='update_quantity'),

]
