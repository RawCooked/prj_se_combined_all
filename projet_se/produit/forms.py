from django import forms
from .models import Produit
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom_produit', 'description_produit', 'image_produit', 'categorie_produit', 'quantite_produit', 'prix_produit', 'fournisseur_produit']




