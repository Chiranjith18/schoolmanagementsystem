from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework import permissions
from schoolmanagement import views
from django.views.generic import TemplateView  # ✅ ADDED for home page



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/academics/', include('academics.urls')),
   
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

   
    
    # ✅ FIXED: Proper home page (login)
    path('', views.home, name='home'),
    
    # ✅ FIXED: Order doesn't matter now since academics.urls has dashboard paths
]

# ✅ REMOVED: Duplicate dashboard paths - now handled in academics.urls
