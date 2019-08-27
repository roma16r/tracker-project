from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Project
from tracker.apps.task.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse_lazy


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    paginate_by = 15

    def get_queryset(self):
        current_user = self.request.user
        query = Project.objects.prefetch_related('users').order_by('-id')
        if current_user.groups.filter(name='admin').exists() or current_user.is_superuser:
            return query.all()
        return query.filter(users__id=current_user.pk)


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'slug', 'users', 'description']
    template_name = 'project/project_new.html'
    permission_required = 'project.add_project'

    def form_valid(self, form):
        if form.cleaned_data['slug'] == 'new':
            form.add_error('slug', 'Not allowed slug.')
            return self.form_invalid(form)
        return super(ProjectCreateView, self).form_valid(form)


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'slug', 'users', 'description']
    template_name = 'project/project_update.html'
    permission_required = 'project.change_project'

    def form_valid(self, form):
        if form.cleaned_data['slug'] == 'new':
            form.add_error('slug', 'Not allowed slug.')
            return self.form_invalid(form)
        return super(ProjectUpdateView, self).form_valid(form)


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects')
    permission_required = 'project.delete_project'


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView, MultipleObjectMixin):
    model = Project
    context_object_name = 'project'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        object_list = Task.objects.prefetch_related('creator', 'executor').order_by('-id').\
            filter(project=self.get_object())
        return super(ProjectDetailView, self).get_context_data(object_list=object_list, **kwargs)

    def test_func(self):
        current_user = self.request.user
        if current_user.groups.filter(name='admin').exists() or current_user.is_superuser:
            return True
        return Project.users.through.objects.filter(user_id=current_user.pk, project_id=self.get_object().pk).exists()




