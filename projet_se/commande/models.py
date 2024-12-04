from django.db import models
from users.models import User
from produit.models import Produit

class Commande(models.Model):
    produit_commande = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="commandes")
    user_commande = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commandes")
    date_commande = models.DateField(auto_now=True)
    date_livraison = models.DateField(null=True, blank=True)
    methode_livraison = models.CharField(max_length=50, default='Express', blank=True, null=True)
    adresse_livraison = models.CharField(max_length=100, default='', blank=True, null=True)
    quantite_commande = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)  # To differentiate between cart and confirmed orders
    comments= models.CharField(max_length=1000, default='', blank=True, null=True)

    def __str__(self):
        return f"Commande of {self.quantite_commande} {self.produit_commande.nom_produit} by {self.user_commande.username}"
