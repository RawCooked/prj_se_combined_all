from django.urls import path
from . import views
from produit import views as users_views  # Importer les vues du module evaluation


urlpatterns = [
    path('', views.evaluation_list, name='evaluation_list'),
    path('Evaluation/<int:pk>/', views.evaluation_detail, name='evaluation_detail'),
    path('edit/<int:pk>/', views.evaluation_update, name='evaluation_update'),
    path('delete/<int:pk>/', views.evaluation_delete, name='evaluation_delete'),
    path('produit/<int:product_id>/Evaluation/', views.product_evaluation, name='product_evaluation'),
    path('produit/<int:id>/', users_views.produit_detail, name='produit_detail'),  # Expects 'id' as the keyword

    path('new/<int:product_id>/', views.create_evaluation, name='evaluation_create'),
    



]
