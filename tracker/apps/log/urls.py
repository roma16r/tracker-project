from django.urls import path
from .views import LogListView, LogCreateView, LogUpdateView, LogDeleteView

urlpatterns = [
      path('task/<int:pk>/logs', LogListView.as_view(), name='logs'),
      path('task/<int:pk>/log/new', LogCreateView.as_view(), name='log-new'),
      path('task/<int:task_pk>/log/<int:pk>/update', LogUpdateView.as_view(), name='log-update'),
      path('log/<int:pk>/delete', LogDeleteView.as_view(), name='log-delete')
]
