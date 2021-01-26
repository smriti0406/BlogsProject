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
            users = User.objects.get(username=request.POST['search'])
        except(KeyError, User.DoesNotExist):
            users = []
        return HttpResponseRedirect(reverse('Messenger:messenger-newchat', kwargs={'users': users}))
    users = User.objects.all()
    return render(request, 'Messenger/start_chat.html', {'users': users})



