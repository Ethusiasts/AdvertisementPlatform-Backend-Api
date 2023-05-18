"""advertisement_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user.urls')),
    path('api/v1/advertisements/', include('advertisement.urls')),
    path('api/v1/billboards/', include('billboard.urls')),
    path('api/v1/media_agencies/', include('media_agency.urls')),
    path('api/v1/proposals/', include('proposal.urls')),

    path('swagger/', schema_view.with_ui(
        'swagger'), name='schema-swagger-ui')

]
