from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Log
from tracker.apps.task.models import Task
from tracker.apps.project.models import Project
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin


class LogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Log
    context_object_name = 'logs'
    paginate_by = 15

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs.get('pk', None))
        return super(LogListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(LogListView, self).get_context_data(task=self.task, has_perm_add_log=self._has_perm_add_log(), **kwargs)

    def get_queryset(self):
        return Log.objects.filter(task_id=self.kwargs.get('pk')).order_by('-id')

    def test_func(self):
        current_user = self.request.user
        if current_user.groups.filter(name='admin').exists() or current_user.is_superuser:
            return True
        return Project.users.through.objects.filter(user_id=current_user.pk,
                                                    project_id=self.task.project.pk).exists()

    def _has_perm_add_log(self):
        current_user = self.request.user
        if current_user.groups.filter(name='admin').exists() or current_user.is_superuser:
            return True
        return self.task.executor_id == current_user.pk


class LogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Log
    fields = ['spent_time', 'comment']
    template_name = 'log/log_new.html'

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs.get('pk', None))
        return super(LogCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.task_id = self.kwargs['pk']
        return super().form_valid(form)

    def test_func(self):
        current_user = self.request.user
        if current_user.groups.filter(name='admin').exists() or current_user.is_superuser:
            return True
        return self.task.executor_id == current_user.pk


class LogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Log
    fields = ['spent_time', 'comment']
    template_name = 'log/log_update.html'
    permission_required = 'log.change_log'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Task, pk=self.kwargs.get('task_pk', None))
        return super(LogUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.task_id = self.kwargs['task_pk']
        return super().form_valid(form)


class LogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Log
    permission_required = 'log.delete_log'

    def get_success_url(self):
        return self.request.GET.get('next', '/')




