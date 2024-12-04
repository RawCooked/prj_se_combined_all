from django.shortcuts import render, get_object_or_404, redirect
from .models import Evaluation
from .forms import EvaluationForm
from produit.models import Produit
from users.models import User
from django.shortcuts import render, redirect

def evaluation_list(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'Evaluation/Evaluation_list.html', {'evaluations': evaluations})

def evaluation_detail(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    return render(request, 'Evaluation/Evaluation_detail.html', {'evaluation': evaluation})

def create_evaluation(request, product_id):
    product = get_object_or_404(Produit, id=product_id)  # Récupérer le produit par son ID
    if not request.user.is_authenticated:
        # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
        return redirect('login')
    
    if request.method == 'POST':
        form = EvaluationForm(request.POST, product_id=product.id)  # Créer le formulaire avec les données POST et l'ID du produit
        if form.is_valid():
            # Si le formulaire est valide, créer l'évaluation
            evaluation = form.save(commit=False)
            evaluation.produit = product  # Associer l'évaluation au produit
            evaluation.utilisateur = request.user  # Associer l'évaluation à l'utilisateur connecté
            evaluation.save()  # Sauvegarder l'évaluation
          #  return redirect('Evaluation_list', product_id=product.id)  # Rediriger vers la page du produit
            return redirect('evaluation_list')  # Rediriger vers la liste des évaluations après la sauvegarde

    else:
        # Si la requête est en GET, afficher le formulaire vide
        form = EvaluationForm(product_id=product.id)
    
    # Rendu de la page avec le formulaire
    return render(request, 'Evaluation/Evaluation_form.html', {'form': form, 'product': product})

def evaluation_update(request, pk):
    # Récupérer l'évaluation à mettre à jour
    evaluation = get_object_or_404(Evaluation, pk=pk)
    product = evaluation.produit  # Récupérer le produit associé à cette évaluation

    if request.method == 'POST':
        # Initialiser le formulaire avec les données POST et l'instance de l'évaluation
        form = EvaluationForm(request.POST, instance=evaluation)
        
        if form.is_valid():
            # Enregistrer l'évaluation après avoir associé le produit et l'utilisateur
            updated_evaluation = form.save(commit=False)
            updated_evaluation.produit = product  # L'ID du produit est automatiquement associé
            updated_evaluation.utilisateur = request.user  # L'ID de l'utilisateur est automatiquement associé
            
            updated_evaluation.save()  # Sauvegarder l'évaluation mise à jour
            return redirect('evaluation_list')  # Rediriger vers la liste des évaluations après la sauvegarde
        else:
            # Si le formulaire n'est pas valide, afficher les erreurs
            print("Form Errors:", form.errors)
    
    else:
        # Si la requête est en GET, afficher le formulaire pré-rempli avec les données de l'évaluation
        form = EvaluationForm(instance=evaluation)
    
    # Rendu de la page avec le formulaire
    return render(request, 'Evaluation/Evaluation_form.html', {'form': form, 'product': product})


def evaluation_delete(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        evaluation.delete()
        return redirect('evaluation_list')
    return render(request, 'Evaluation/Evaluation_confirm_delete.html', {'evaluation': evaluation})


from .models import Produit, Evaluation
from .forms import EvaluationForm

def product_evaluation(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)
    evaluation_existante = Evaluation.objects.filter(produit=produit, utilisateur=request.user).first()

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            if evaluation_existante:
                # Si une évaluation existe déjà, on met à jour la note et le commentaire
                evaluation_existante.note = form.cleaned_data['note']
                evaluation_existante.commentaire = form.cleaned_data['commentaire']
                evaluation_existante.save()
            else:
                # Si aucune évaluation n'existe, on en crée une nouvelle
                form.instance.produit = produit
                form.instance.utilisateur = request.user
                form.instance.type_evaluation = 'Produit'  # Vous pouvez ajuster le type si nécessaire
                form.save()
            return redirect('product_evaluation', product_id=produit.id)  # Rediriger après soumission
    else:
        form = EvaluationForm(instance=evaluation_existante)  # Pré-remplir si l'avis existe déjà

    return render(request, '../produit/templates/produit/produit_detail.html', {'form': form, 'produit': produit})



# LES METIERS BASIQUE


def evaluation_list(request):
    # Récupérer la valeur de recherche (si présente)
    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', '')

    # Filtrer les évaluations en fonction de la recherche
    evaluations = Evaluation.objects.all()

    if search_query:
        evaluations = evaluations.filter(commentaire__icontains=search_query)

    # Trier les évaluations en fonction de l'option choisie
    if sort_option == 'date':
        evaluations = evaluations.order_by('date_evaluation')
    elif sort_option == 'note':
        evaluations = evaluations.order_by('-note')

    return render(request, 'Evaluation/evaluation_list.html', {'evaluations': evaluations})
