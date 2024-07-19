from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', log_out, name='logout'),
    path('profile/', prof_user, name='profile'),
    path('profile/edit/', prof_edit, name='edit'),
    path('users/', user_list, name='ulist'),
    path('users/<int:pk>/', user_detail, name='udet'),
    path('private/', priv_list, name='private'),
    path('private/<str:room>/', priv_chat),
    path('rooms/', room_list, name='public'),
    path('rooms/<slug:slug>/', pub_chat),
    ]