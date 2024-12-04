from django.db import models
from users.models import User 
from django.db.models import Avg  # Pour utiliser l'agrégation


class Produit(models.Model):
    # id_produit sera un champ auto-incrémenté par défaut si on ne le définit pas
    # C'est la configuration par défaut pour la clé primaire
    proprietaire = models.ForeignKey(User,on_delete=models.CASCADE)
    nom_produit = models.CharField(max_length=100)
    description_produit = models.TextField()
    image_produit = models.ImageField(upload_to='images/', blank=True, null=True)
    categorie_produit = models.CharField(max_length=50)
    quantite_produit = models.PositiveIntegerField(default=0)
    prix_produit = models.DecimalField(max_digits=10, decimal_places=2)
    fournisseur_produit = models.CharField(max_length=100)

#***************METIER EVALUATION*********************
    def moyenne_notes(self):
        # Calculer la moyenne des notes des évaluations pour ce produit
        evaluations = self.evaluation_set.all()  # Récupérer toutes les évaluations associées à ce produit
        if evaluations.exists():
            # Utiliser l'agrégation pour calculer la moyenne des notes
            return evaluations.aggregate(Avg('note'))['note__avg']
        else:
            return None  # Aucun évaluation, donc pas de moyenne
#******************************************************

    
    def __str__(self):
        return self.nom_produit
    
   



