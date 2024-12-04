import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from .forms import MessageForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
# Afficher la liste des messages
@login_required
def message_list(request):
    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messages_list.html', {'messages': messages})

# Afficher le détail d'un message
@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    return render(request, 'message_detail.html', {'message': message})

@csrf_exempt  # Assurez-vous d'utiliser le middleware CSRF pour la production
@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Extraire les données JSON
            content = data.get('content')
            recipient_id = data.get('recipient_id')

            if not content:
                return JsonResponse({'success': False, 'error': 'Le contenu du message est vide'})

            recipient = get_object_or_404(User, pk=recipient_id)
            sender = request.user

            # Créer le message
            message = Message.objects.create(
                sender=sender,
                recipient=recipient,
                content=content,
                created_at=timezone.now()
            )

            return JsonResponse({
                'success': True,
                'sender': sender.username,
                'recipient': recipient.username,
                'content': message.content,
                'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Données JSON invalides'})
    return JsonResponse({'success': False, 'error': 'Méthode de requête invalide'})

# Mettre à jour un message existant
@login_required
@csrf_exempt
def update_message(request, message_id):
    if request.method == 'PUT':
        try:
            # Charger les données JSON depuis request.body
            data = json.loads(request.body)

            # Accéder au contenu du message
            content = data.get('content', '')

            # Vérifier si le contenu est vide
            if not content:
                return JsonResponse({'error': 'Content cannot be empty'}, status=400)

            # Mettez à jour le message avec l'ID spécifié
            message = Message.objects.get(id=message_id)
            message.content = content
            message.save()

            return JsonResponse({'message': 'Message updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
# Supprimer un message
@login_required
def delete_message(request, message_id):
    try:
        # Récupérer le message avec l'ID spécifié
        message = get_object_or_404(Message, id=message_id)
        
        # Supprimer le message
        message.delete()
        
        return JsonResponse({'success': True})
    
    except Message.DoesNotExist:
        # Retourner une réponse en cas d'erreur si le message n'est pas trouvé
        return JsonResponse({'error': 'Message not found'}, status=404)
User = get_user_model()

def search_users(request):
    query = request.GET.get('q', '')
    if query:
        # Filtrer les utilisateurs par nom d'utilisateur
        users = User.objects.filter(username__icontains=query).values('id', 'username')
    else:
        users = User.objects.none()  # Aucun utilisateur si la recherche est vide

    return JsonResponse(list(users), safe=False)

def get_messages(request):
    user_id = request.GET.get('userId')
    recipient_id = request.GET.get('recipientId')

    if user_id and recipient_id:
        messages = Message.objects.filter(
            sender_id__in=[user_id, recipient_id],
            recipient_id__in=[user_id, recipient_id]
        ).order_by('created_at')
        
        message_list = [
            {
                'id': message.id,
                'sender': message.sender.username,
                'sender_id': message.sender.id,  # Ajout de l'ID de l'expéditeur
                'recip_id': message.recipient.id,  # Ajout de l'ID de l'expéditeur
                'content': message.content,
                'created_at': message.created_at
            } 
            for message in messages
        ]
        return JsonResponse({'messages': message_list})

    return JsonResponse({'error': 'Invalid request'})

def search_messages(request):
    if request.method == 'GET':
        search_term = request.GET.get('search', '').strip().lower()  # Récupérer le terme de recherche depuis l'URL
        
        # Filtrer les messages en fonction du contenu
        if search_term:
            messages = Message.objects.filter(content__icontains=search_term)
        else:
            messages = Message.objects.all()
        
        # Optionnel : rendre les messages sous forme de dictionnaire pour la réponse JSON
        message_list = [{'sender': msg.sender.username, 'content': msg.content, 'created_at': msg.created_at} for msg in messages]

        return JsonResponse({'messages': message_list}, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)