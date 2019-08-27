from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', TemplateView.as_view(template_name='homepage.html'), name="homepage"),
    path('admin/', admin.site.urls),
    path('', include('tracker.apps.user.urls')),
    path('', include('tracker.apps.project.urls')),
    path('', include('tracker.apps.task.urls')),
    path('', include('tracker.apps.log.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


