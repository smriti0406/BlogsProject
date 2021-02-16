from django.shortcuts import render, get_object_or_404
from .models import ChatRoom, ChatMessage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from djongo.models import Q
# Create your views here.


@login_required
def index(request):
    query = Q(first=request.user) | Q(second=request.user)
    try:
        chat_rooms = ChatRoom.objects.filter(query).order_by('-timeCreated')
    except(KeyError, ChatMessage.DoesNotExist):
        chat_rooms = []
    return render(request, 'Messenger/index.html', {'chat_rooms': chat_rooms})


@login_required
def chatroom(request, chatroom_id):
    chat_room = ChatRoom.objects.get(pk=chatroom_id)
    if request.method == 'POST':
        ChatMessage.objects.create(chatRoom=chat_room, author=request.user, message=request.POST['message'])
        return HttpResponseRedirect(reverse('Messenger:messenger-chatroom', kwargs={'chatroom_id': chat_room.id}))
    return render(request, 'Messenger/chat_room.html', {'chat_room': chat_room})


@login_required
def newchat(request):
    if request.method == "POST":
        try:
            users = User.objects.filter(username__contains=request.POST['search']).exclude(username=request.user.username)
        except(KeyError, User.DoesNotExist):
            users = []
        return render(request, 'Messenger/start_chat.html', {'users': users})

    users = User.objects.all()
    return render(request, 'Messenger/start_chat.html', {'users': users})


@login_required
def createchat(request, friend_id):
    friend = get_object_or_404(User, pk=friend_id)
    if friend is request.user:
        return HttpResponseRedirect(reverse('Messenger:messenger-index'))
    query = (Q(first=request.user) & Q(second=friend)) | (Q(first=friend) & Q(second=request.user))
    try:
        chatroom = ChatRoom.objects.get(query)
    except(KeyError, ChatRoom.DoesNotExist):
        chatroom = ChatRoom.objects.create(first=request.user, second=friend)

    return HttpResponseRedirect(reverse('Messenger:messenger-chatroom', kwargs={'chatroom_id': chatroom.id}))




