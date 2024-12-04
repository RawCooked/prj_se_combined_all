# forms.py
from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = [ 'methode_livraison', 'adresse_livraison', 'quantite_commande']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['adresse_livraison', 'methode_livraison', 'quantite_commande', 'date_livraison', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
            'date_livraison': forms.DateInput(attrs={'type': 'date'}),  # Make sure the date input is properly handled
        }

    # You can also add any additional validation if needed
    def clean_quantite_commande(self):
        quantite = self.cleaned_data.get('quantite_commande', 1)
        if quantite < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantite