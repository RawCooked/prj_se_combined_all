from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('etablissement_dashboard/', views.etablissement_dashboard, name='etablissement_dashboard'),
        path('messages/', views.messages_list_view, name='messages_list'),
            path('shop/', views.shop_view, name='shop'),
            path('Evaluation/', views.ev_list_view, name='ev'),
            path('update_client/', views.update_client, name='update_client'),
            path('list_users/', views.liste_users, name='liste_users'),
            path('profile/', views.profile, name='profile'),
            path('profil/<str:email>/', views.profil_user, name='profil_user'),
                path('add_to_cart/<int:produit_id>/', views.add_to_cart, name='add_to_cart'),
    path('commande_dashboard/', views.commande_dashboard, name='commande_dashboard'),
    path('delete_command/<int:id>/', views.delete_command, name='delete_command'),
    path('process_checkout/', views.process_checkout, name='process_checkout'),
    path('update-cart/<int:commande_id>/', views.update_cart, name='update_cart'),
    path('click_button_summ/',views.click_button_summ,name='click_button_summ'),
    path('save_user_purchases/',views.save_user_purchases,name='save_user_purchases'),
    path('remove_quantity/<int:id>/',views.remove_quantity,name='remove_quantity'),
    path('add_quantity/<int:id>/',views.add_quantity,name='add_quantity'),



    
]
