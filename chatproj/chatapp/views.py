from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework.response import Response

from .forms import RegForm, LoginForm, EditForm
from .models import *
from rest_framework import viewsets, status


from .serializers import PublicSerializer
from .permissions import IsOwnerOrReadOnly


# Create your views here.
def home(request):
    user = request.user
    return render(request, 'home.html', {'user': request.user})


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        form = RegForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=username, password=password).save()
            return redirect(to='login')
        return render(request, 'accounts/signup.html', {'form': form})
    else:
        print(request.session)
        form = RegForm
        return render(request, 'accounts/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'accounts/user_error.html')
        return redirect(to='home')
    if request.method == 'GET':
        form = LoginForm
        return render(request, 'accounts/login.html', {'form': form})


@login_required
def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect(to='home')
    else:
        print('check')
        return render(request, 'accounts/logout.html')


@login_required
def prof_user(request):
    return render(request, 'accounts/profile.html', {'username': request.user.username,
                                                     'nickname': request.user.nickname,
                                                     'avatar': request.user.avatar, })


@login_required
def prof_edit(request):
    if request.method == 'POST':
        user = request.user
        old_ava = user.avatar
        old_nick = user.nickname
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            nick = form.cleaned_data["nickname"]
            if not nick:
                nick = old_nick
            ava = form.cleaned_data["avatar"]
            print(ava, nick)
            if not ava:
                ava = old_ava
            obj = User.objects.get(username=user.username)
            obj.nickname = nick
            obj.avatar = ava
            obj.save()
        return redirect(to='profile')
    else:
        form = EditForm
        return render(request, 'accounts/edit.html', {'form': form})


def user_list(request):
    u_list = User.objects.all().filter(is_staff=0)
    return render(request, 'userlist.html', {'ulist': u_list})


def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    guest = request.user
    path = f'{user.nickname}_to_{guest.nickname}'
    if request.user.pk == user.pk:
        return redirect(to='profile')
    return render(request, 'user_detail.html', {'user': user,
                                                'path': path})


@login_required
def priv_chat(request, room):
    user = request.user
    path = request.path
    list_users = room.split('_to_')
    list_users.remove(user.nickname)
    opp_user_nick = list_users[0]
    opp_user = User.objects.get(nickname=opp_user_nick)
    if PrivetChat.objects.all().filter(chat_path=path):
        print("ok")
    else:
        chat = PrivetChat.objects.create(chat_path=path, user1=user, user2=opp_user)
    return render(request, 'chat.html', {'room_name': room,
                                         'user_name': user.nickname,
                                         'opp': opp_user,
                                         })


@login_required
def priv_list(request):
    user = request.user
    chats = PrivetChat.objects.all().filter(Q(user1=user) | Q(user2=user))
    return render(request, 'priv_list.html', {'chats': chats,
                                              'user': user})


@login_required
def room_list(request):
    rooms = PublicChat.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})


@login_required
def pub_chat(request, slug):
    user = request.user
    chat = PublicChat.objects.get(slug=slug)
    return render(request, 'pub_chat.html', {'room_name': slug,
                                             'user_name': user.nickname,
                                             'chat': chat})


class PublicViewSet(viewsets.ModelViewSet):
    queryset = PublicChat.objects.all()
    serializer_class = PublicSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.owner and request.user:
                self.perform_destroy(instance)
            else:
                print('no')
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
