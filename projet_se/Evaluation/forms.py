from django import forms
from .models import Evaluation
from .models import Produit


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['note', 'commentaire']  # Include the necessary fields for the evaluation
    
     # Ajouter un champ caché pour l'ID du produit
    product_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # Le rendre non requis

    def __init__(self, *args, **kwargs):
        # Récupérer l'ID du produit passé à la vue
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        if product_id:
            # Si un ID de produit est passé, initialiser ce champ avec l'ID du produit
            self.fields['product_id'].initial = product_id