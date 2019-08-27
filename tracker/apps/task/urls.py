from django.urls import path
from .views import TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView
from . import views


urlpatterns = [
      path('project/<slug:slug>/task/new', TaskCreateView.as_view(), name='task-new'),
      path('task/<int:pk>', TaskDetailView.as_view(), name='task-detail'),
      path('project/<slug:slug>/task/<int:pk>/update', TaskUpdateView.as_view(), name='task-update'),
      path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete')
]
