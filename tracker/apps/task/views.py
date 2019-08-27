from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .models import Task
from tracker.apps.project.models import Project
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic.edit import FormMixin
from .forms import TaskForm, CommentForm
from django.db.models import Sum
from django.db.models.functions import Coalesce


class TaskCreateView(PermissionRequiredMixin, CreateView):
    model = Task
    template_name = 'task/task_new.html'
    form_class = TaskForm
    permission_required = 'task.add_task'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=self.kwargs.get('slug', None))
        return super(TaskCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.project = get_object_or_404(Project, slug=self.kwargs.get('slug', None))

        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'task/task_update.html'
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=self.kwargs.get('slug', None))
        return super(TaskUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def test_func(self):
        return _update_detail_permission(self)


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    model = Task
    permission_required = 'task.delete_task'

    def get_success_url(self):
        return self.request.GET.get('next', '/')


class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
    model = Task
    context_object_name = 'task'
    form_class = CommentForm
    queryset = Task.objects.prefetch_related('comment_set__user').\
        annotate(spent_time_total=Coalesce(Sum('log__spent_time'), 0))

    def get_context_data(self, **kwargs):
        comment_form = CommentForm(initial={'task': self.object, 'user': self.request.user})
        return super(TaskDetailView, self).get_context_data(comment_form=comment_form, **kwargs)

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(TaskDetailView, self).form_valid(form)

    def test_func(self):
        return _update_detail_permission(self)


def _update_detail_permission(self):
    current_user = self.request.user
    if current_user.groups.filter(name='admin').exists() or current_user.is_superuser:
        return True
    return Project.users.through.objects.filter(user_id=current_user.pk,
                                                project_id=self.get_object().project.pk).exists()
