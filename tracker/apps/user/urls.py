from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserListView, UserCreateView, UserDetailView, UserDeleteView, UserUpdateView, ProfileUpdateView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users', UserListView.as_view(), name='users'),
    path('user/new', UserCreateView.as_view(), name='user-new'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name='user-delete'),
    path('user/<int:pk>/update', UserUpdateView.as_view(), name='user-update'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update')
]
