"""placasvirtuais URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from allauth.account.views import LoginView
from core.forms import AllauthCompatLoginForm


urlpatterns = [
    path('', include('core.urls')),
    path('boards/', include('board.urls')),
    path('courses/', include('course.urls')),
    path('campus/', include('campus.urls')),
    path('egress/', include('egress.urls')),
    path('sending/', include('sending.urls')),
    path('users/', include('core.urls', namespace='v1')),
    path('admin/', admin.site.urls),
    path(
        'accounts/login/',
        LoginView.as_view(form_class=AllauthCompatLoginForm),
        name="account_login"
    ),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

