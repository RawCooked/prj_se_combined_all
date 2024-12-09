
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm
# # Create your views here.
# from django.shortcuts import render, redirect
# from .forms import UserRegistrationForm

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Rediriger vers la page de login après l'inscription
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'users/register.html', {'form': form})
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             if user.status == 'client':
#                 return redirect('client_dashboard')  # Page de bienvenue pour le client
#             elif user.status == 'etablissement':
#                 return redirect('etablissement_dashboard')  # Page de bienvenue pour l'établissement
#     else:
#         form = AuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})

# @login_required
# def client_dashboard(request):
#     return render(request, 'users/client_dashboard.html', {'user': request.user})

# @login_required
# def etablissement_dashboard(request):
#     return render(request, 'users/etablissement_dashboard.html', {'user': request.user})
# views.py

from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, EmailAuthenticationForm
from produit.models import Produit
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from commande.models import  Commande




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from commande.forms import CommandeForm



from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, EmailAuthenticationForm


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import UpdateClientForm  # Créez ce formulaire séparément
from django.contrib.auth.models import User






from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, EmailAuthenticationForm


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import UpdateClientForm  # Créez ce formulaire séparément
from django.contrib.auth.models import User
import smtplib
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
from django.http import JsonResponse, HttpResponseRedirect
import os

import csv


from django.http import FileResponse



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Rediriger vers la page de login après l'inscription
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.status == 'client':
                return redirect('client_dashboard')
            elif user.status == 'etablissement':
                return redirect('etablissement_dashboard')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def commande_dashboard(request):

    commande=Commande.objects.filter(user_commande=request.user, is_ordered=False)
    commande_ordered= Commande.objects.filter(user_commande=request.user, is_ordered=True)
    tot=0
    for comm in commande :
        tot += comm.quantite_commande * comm.produit_commande.prix_produit
    
    context = {
        'commandes': commande,  # Pass the form to the template
        'total':tot,
        'commande_ordered' : commande_ordered
    }

    return render(request, 'users/shoping-cart.html', context)

def delete_command(request, id):
    # Check if the request is a POST request
    if request.method == "POST":
        # Retrieve the specific command by ID
        commande = get_object_or_404(Commande, id=id)
        # Delete the command
        commande.delete()
        # Redirect back to the page with the command list
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # If the request is not POST, redirect to the list page or show an error
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def process_checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            # Check if an order already exists for the user (if it's a cart order, for example)
            commande_id = request.POST.get('commande_id', None)

            if commande_id:  # Update an existing order if 'commande_id' is passed
                try:
                    commande = Commande.objects.get(id=commande_id, user_commande=request.user)
                except Commande.DoesNotExist:
                    messages.error(request, "Order not found.")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:  # If no 'commande_id', create a new order
                commande = Commande(user_commande=request.user)  # Create new order instance

            # Update the fields with the form data
            commande.adresse_livraison = form.cleaned_data.get('adresse_livraison')
            commande.methode_livraison = form.cleaned_data.get('methode_livraison')
            commande.quantite_commande = form.cleaned_data.get('quantite_commande', 1)  # Default to 1
            commande.date_livraison = form.cleaned_data.get('date_livraison', None)

            # Additional fields (for example, payment info or comments) can also be added here
            # commande.comments = form.cleaned_data.get('comments', '')

            # Mark the order as confirmed if it's a final checkout (can be set via a form field or logic)
            if 'is_ordered' in form.cleaned_data:
                commande.is_ordered = form.cleaned_data['is_ordered']

            # Save the updated or newly created order
            commande.save()  # This will either update or create the 'commande' in the database

            # Add a success message
            messages.success(request, "Your order has been placed successfully!")

            # Redirect to the referring page (e.g., order confirmation page)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        else:
            # If the form is invalid, show error messages
            messages.error(request, "Please check the form and try again.")
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})

def update_cart(request):
    if request.method == 'POST':
        command_id = request.POST.get('command_id')
        address = request.POST.get('adresse_livraison')
        delivery_method = request.POST.get('methode_livraison')

        # Find the corresponding Commande based on the command_id
        commande = Commande.objects.get(id=command_id, user_commande=request.user)

        # Update the values
        commande.adresse_livraison = address
        commande.methode_livraison = delivery_method
        commande.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

import smtplib
@login_required
def click_button_summ(request):

        
    """ # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("pcg6647@gmail.com", "cgln unof evey qmqq")
    # message to be sent

    message = "hello Mr " + request.user.first_name + " " + request.user.last_name + " you have ordered some products ."
    # sending the mail
    s.sendmail("pcg6647@gmail.com", request.user.email , message)
    # terminating the session
    s.quit() """

    commande=Commande.objects.filter(user_commande=request.user, is_ordered=False)

    for comm in commande :
        comm.is_ordered=True
        comm.save()
    
        Livraison.objects.create(
                commande=comm,
                state=Livraison.DeliveryState.PENDING  # Default state is pending
            )
      

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@login_required
def add_to_cart(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    # Check if the product is already in the cart
    commande, created = Commande.objects.get_or_create(
        produit_commande=produit,
        user_commande=request.user,
        is_ordered=False,
    )

    if not created:  # If the product is already in the cart, increment the quantity
        commande.quantite_commande += 1
        commande.save()
        messages.info(request, f"{produit.nom_produit} quantity increased in your cart.")
    else:
        messages.success(request, f"{produit.nom_produit} has been added to your cart.")
    
    # Redirect to the referring page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@login_required
def save_user_purchases(request):
    # Fetch all purchases for the specified user
    products = Commande.objects.filter(user_commande__id=request.user.id, is_ordered=True)

    # Define the file name and path
    file_name = f"user_{request.user.first_name}_purchases.csv"
    file_path = os.path.join("exports", file_name)  # Use a specific directory for exports

    # Ensure the directory exists
    os.makedirs("exports", exist_ok=True)

    # Write to the CSV file
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(["Product Name", "Quantity", "Ordered Date"])

        # Write each product's data
        for product in products:
            writer.writerow([
                product.produit_commande.nom_produit,
                product.quantite_commande,
                product.date_commande,
            ])

    # Serve the file for download
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename=file_name)


def log_pdf(request):
    # Get all commands for the logged-in user
    commandes = Commande.objects.filter(user_commande=request.user)
    
    # Extract product names from commandes
    produits = [commande.produit_commande.nom_produit for commande in commandes]
    
    # Save the user's purchases
    save_user_purchases(request.user.first_name, produits)

    # Redirect the user to the previous page
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def add_quantity(request, id):
    # Retrieve the specific Commande instance or return a 404 error
    commande = get_object_or_404(Commande, id=id)

    # Increment the quantity
    commande.quantite_commande += 1

    # Save the updated instance
    commande.save()

    # Redirect back to the previous page or a default fallback URL
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def remove_quantity(request,id):
    commande = get_object_or_404(Commande, id=id)
    if commande.quantite_commande > 1 :
        commande.quantite_commande -= 1

    commande.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))




@login_required
def etablissement_dashboard(request):
    return render(request, '../static/index.html', {'user': request.user})

def messages_list_view(request):
    return render(request, '../templates/messages_list.html')

def ev_list_view(request):
    return render(request, 'Evaluation/Evaluation_list.html')

def shop_view(request):
    return render(request, 'produit/produit_list.html') 


@login_required
def update_client(request):
    user = request.user  # Récupérer l'utilisateur connecté

    if request.method == 'POST':
        form = UpdateClientForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vos informations ont été mises à jour avec succès.')
            return redirect('update_client')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = UpdateClientForm(instance=user)

    return render(request, 'users/update_client.html', {'form': form})

# from django.contrib.auth import get_user_model
# def liste_users(request):
#     query = request.GET.get('q')  # Récupérer la valeur saisie dans la barre de recherche
#     if query:
#         users = User.objects.filter(email__icontains=query)  # Filtrer les utilisateurs par email
#     else:
#         User = get_user_model()
#         users = User.objects.all()  # Afficher tous les utilisateurs
#     return render(request, 'users/listeusers.html', {'users': users})

from django.contrib.auth import get_user_model

def liste_users(request):
    User = get_user_model()
    query = request.GET.get('query', '')  # Récupère la recherche de l'utilisateur
    if query:
        users = User.objects.filter(email__icontains=query)  # Filtrer les utilisateurs par email
    else:
        users = User.objects.all()  # Afficher tous les utilisateurs
    return render(request, 'users/listeusers.html', {'users': users, 'query': query})





@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})



from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model  # Récupérer le bon modèle utilisateur

def profil_user(request, email):
    # Récupérer le modèle utilisateur (personnalisé ou par défaut)
    User = get_user_model()
    
    # Récupérer l'utilisateur par email
    user = get_object_or_404(User, email=email)
    
    # Passer les informations de l'utilisateur au template
    return render(request, 'users/profil.html', {'user': user})




from livraison.models import Livraison


@login_required
def livraisons(request):
    livraisons = Livraison.objects.filter(commande__user_commande=request.user)
    #livraisons = Livraison.objects.filter(  )
    is_admin = True # Example condition to check if the user is admin

    context = {
        'livraisons': livraisons,
        'is_admin': is_admin,
    }
    return render(request, 'users/livraison.html', context)

@login_required
def client_dashboard(request):
    produits = Produit.objects.all()
    user_orders_count = Commande.objects.filter(user_commande=request.user, is_ordered=False).count()

    
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.user_commande = request.user  # Assign the logged-in user
            commande.save()
            form.save_m2m()  # Save ManyToMany relationships
            messages.success(request, "Your command has been added successfully!")
            return redirect('client_dashboard')  # Redirect back to the dashboard
        else:
            messages.error(request, "There was an error in your submission.")
    else:
        form = CommandeForm()

    context = {
        'count':user_orders_count,
        'produits': produits,
        'form': form,  # Pass the form to the template
    }

    return render(request, 'users/client_dashboard.html', context)

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def switch(request, id):
    # Retrieve the specific Livraison object or return 404 if not found
    livraison = get_object_or_404(Livraison, id=id)
    
    # Define the states in the order of transition
    state_order = [
        Livraison.DeliveryState.PENDING,
        Livraison.DeliveryState.IN_TRANSIT,
        Livraison.DeliveryState.DELIVERED,
        Livraison.DeliveryState.FAILED,
    ]
    
    # Get the index of the current state and determine the next state
    current_index = state_order.index(livraison.state)
    next_index = (current_index + 1) % len(state_order)  # Loop back to the first state if at the end
    livraison.state = state_order[next_index]
    
    # Save the changes
    livraison.save()
    
    # Redirect back to the referring page or to a default URL
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def delete(request,id):

    livraison = get_object_or_404(Livraison, id=id)
    
    # Delete the object
    livraison.delete()
    

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def accept(request,id):

    livraison = get_object_or_404(Livraison, id=id)
    
    # Delete the object
    livraison.delete()
    

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
