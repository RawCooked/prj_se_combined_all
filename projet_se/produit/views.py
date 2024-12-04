from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Produit
from .forms import ProduitForm
from django.core.paginator import Paginator
from Evaluation.models import Evaluation
from Evaluation.forms import EvaluationForm

# List all products with pagination and search
@login_required
def produit_list(request):
        
    sort_by = request.GET.get('sort_by', 'nom_produit')  # Valeur par défaut si rien n'est sélectionné

    # Assurer que sort_by est une valeur valide
    if sort_by not in ['nom_produit', 'prix_produit', 'quantite_produit']:
        sort_by = 'nom_produit'

    produits = Produit.objects.all().order_by(sort_by)  # Appliquer le tri ici


    # Récupérer le paramètre de recherche 'q' (si présent)
    query = request.GET.get('q', '')
    
    # Filtrer les produits selon le nom si la recherche est effectuée
    if query:
        produits = Produit.objects.filter(nom_produit__icontains=query)
    else:
        produits = Produit.objects.all()
        
    # Pagination
    paginator = Paginator(produits, 6)  # Affiche 6 produits par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'produit/produit_list.html', {'page_obj': page_obj})

# Show details of a single product
@login_required
def produit_detail(request, id):
    produit = get_object_or_404(Produit, id=id)
    return render(request, 'produit/produit_detail.html', {'produit': produit})

# Create a new product
@login_required
def produit_create(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form without committing to the database
            produit = form.save(commit=False)
            # Set the owner (proprietaire) to the logged-in user
            produit.proprietaire = request.user
            # Save the product
            produit.save()
            return redirect('produit_list')
    else:
        form = ProduitForm()
    return render(request, 'produit/produit_form.html', {'form': form})

# Update an existing product
@login_required
def produit_update(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produit/produit_form.html', {'form': form})

# Delete a product
@login_required
def produit_delete(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        return redirect('produit_list')
    return render(request, 'produit/produit_confirm_delete.html', {'produit': produit})




#********************METIER EVALUATION******************
def produit_detail(request, id):
    produit = get_object_or_404(Produit, id=id)
    
    # Calculer la moyenne des notes pour ce produit
    moyenne = produit.moyenne_notes()  # Utiliser la méthode du modèle pour obtenir la moyenne
    
    return render(request, 'produit/produit_detail.html', {
        'produit': produit,
        'moyenne': moyenne
    })
#*******************************************************