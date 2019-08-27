from django.urls import path, include
from .views import ProjectListView, ProjectCreateView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView


urlpatterns = [
    path('projects', ProjectListView.as_view(), name='projects'),
    path('project/new', ProjectCreateView.as_view(), name='project-new'),
    path('project/<slug:slug>', ProjectDetailView.as_view(), name='project-detail'),
    path('project/<slug:slug>/update', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<slug:slug>/delete', ProjectDeleteView.as_view(), name='project-delete')
]