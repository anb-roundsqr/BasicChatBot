"""ChatBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from ChatBot.views import (
    ClientConfiguration,
    CustomerViewSet,
    BotViewSet,
    CustomerBotViewSet,
    ClientForm,
    SessionAnalytics,
    AssetsUploader,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'bots', BotViewSet, basename='bots')
router.register(r'customerbots', CustomerBotViewSet, basename='customerbots')

urlpatterns = [
    path(r'', include(router.urls)),
    path('admin/', admin.site.urls),
    re_path(r'client-config', ClientConfiguration.as_view()),
    re_path(r'client-form', ClientForm.as_view()),
    re_path(r'session-analytics/(?P<slug>[\w-]+)', SessionAnalytics.as_view()),
    re_path(r'assets/(?P<slug>[\w-]+)', AssetsUploader.as_view()),
]
