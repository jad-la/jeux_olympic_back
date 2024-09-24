from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events.api_events_docs import CustomSpectacularAPIView
from drf_spectacular.views import  SpectacularSwaggerView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('api/users/', include('users.urls')),
    path('api/', include('tickets.urls')),

    # Ajoute l'URL pour le schéma OpenAPI (nécessaire pour Swagger UI)
     path('api/schema/', CustomSpectacularAPIView.as_view(), name='schema'),
    # URL pour Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
