from django.db import models
from django.contrib.auth.models import User
from users.models import User
from produit.models import Produit


class Evaluation(models.Model):
    # Main attributes
    note = models.IntegerField("Note", choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    commentaire = models.TextField("Commentaire", blank=True, null=True)
    date_evaluation = models.DateTimeField("Date d'évaluation", auto_now_add=True)
    
    # Foreign keys
    utilisateur = models.ForeignKey(User,on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,verbose_name="Produit",on_delete=models.CASCADE,blank=True,null=True)
    #vendeur = models.ForeignKey('Vendeur', verbose_name="Vendeur", on_delete=models.CASCADE, blank=True, null=True)
    
    # Evaluation type
    TYPE_EVALUATION_CHOICES = [
        ('Produit', 'Produit'),
        ('Vendeur', 'Vendeur'),
    ]
    type_evaluation = models.CharField("Type d'évaluation", max_length=20, choices=TYPE_EVALUATION_CHOICES)
    
    
    class Meta:
        verbose_name = "Évaluation"
        verbose_name_plural = "Évaluations"

    def __str__(self):
        return self.commentaire
