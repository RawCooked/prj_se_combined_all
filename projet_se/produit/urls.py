from django.urls import path
from . import views
from Evaluation import views as evaluation_views  # Importer les vues du module evaluation
urlpatterns = [
    path('', views.produit_list, name='produit_list'),
    path('<int:id>/', views.produit_detail, name='produit_detail'),
    path('create/', views.produit_create, name='produit_create'),
    path('<int:id>/update/', views.produit_update, name='produit_update'),
    path('<int:id>/delete/', views.produit_delete, name='produit_delete'),
    path('new/', evaluation_views.create_evaluation, name='evaluation_create'),

]
