from django.urls import path
from . import views



urlpatterns = [
    path('', views.message_list, name='message_list'),
        path('messages/', views.get_messages, name='get_messages'),
    path('search_users/', views.search_users, name='search_users'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('update_message/<int:message_id>/', views.update_message, name='update_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

    path('search-messages/', views.search_messages, name='search_messages'),




]