from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .forms import UserCreateForm, UserUpdateForm, ProfileForm


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    paginate_by = 15
    permission_required = 'user.view_user_list'

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.pk).order_by('-id')


class UserCreateView(PermissionRequiredMixin, CreateView):
    model = User
    template_name = 'user/user_new.html'
    form_class = UserCreateForm
    permission_required = 'user.add_user'


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    template_name = 'user/user_update.html'
    form_class = UserUpdateForm
    permission_required = 'user.change_user'


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users')
    permission_required = 'user.delete_user'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/user_profile.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)




