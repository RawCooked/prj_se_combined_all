from django.http import HttpResponse
from django.template import loader
from .models import Produit,Commande
from django.shortcuts import render
from django.utils import timezone
from .models import User
from django.urls import reverse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def produitcommande_list(request):
    template = loader.get_template('shoping-cart.html')
    produits = Produit.objects.all()  # Query all Produit objects
    commandes = Commande.objects.select_related('produitcommande_list')  # Query Commande objects with related Produit

    context = {
        'produits': produits,
        'commandes': commandes,
    }
    return HttpResponse(template.render(context, request))

def click_button_add_to_commande(request):
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')

        # Retrieve the product by its ID
        produit = get_object_or_404(Produit, id=produit_id)

        # Retrieve the user where the name is "abc"
        user = get_object_or_404(User, nom="abc")  # Assuming 'nom' is the field for the user's name

        # Create the order (commande)
        commande = Commande.objects.create(
            produit=produit,
            user=user,
            quantite_commande=request.POST.get('quantite_commande', 1),  # Assuming the quantity is passed in the form
            date_livraison=request.POST.get('date_livraison')  # Ensure you handle date of delivery correctly
        )

        return redirect('produitcommande_list')  # Redirect to the product list after adding the order

    return render(request, 'produitcommande_list.html')  # Or your appropriate template

def delete_commande(request, id):
    # Check if the request is a POST request
    if request.method == "POST":
        # Retrieve the specific command by ID
        commande = get_object_or_404(Commande, id=id)
        # Delete the command
        commande.delete()
        # Redirect back to the page with the command list
        return redirect(reverse('produitcommande_list'))  # Use the appropriate name for your command list view

    # If the request is not POST, redirect to the list page or show an error
    return redirect(reverse('produitcommande_list'))


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Commande
from .forms import CommandeForm  # Import the form you'll create for editing

from django.shortcuts import redirect


def edit_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            # Redirection vers la page 'produitcommande_list' après la soumission
            return redirect('produitcommande_list')
    else:
        form = CommandeForm(instance=commande)

    return render(request, 'edit_commande.html', {'form': form})

def update_quantity(request, commande_id):
    if request.method == 'POST':
        # Get the new quantity from the request
        data = json.loads(request.body)
        new_quantity = data.get('quantity')

        # Get the commande object and update the quantity
        commande = Commande.objects.get(id=commande_id)
        commande.quantite_commande = new_quantity
        commande.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)