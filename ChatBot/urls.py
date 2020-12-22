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
from ChatBot import views as vu
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', vu.CustomerViewSet, basename='customers')
router.register(r'bots', vu.BotViewSet, basename='bots')
router.register(r'customerbots', vu.CustomerBotViewSet, basename='customerbots')

urlpatterns = [
    path(r'', include(router.urls)),
    path('admin/', admin.site.urls),
    path('admin/create', vu.register_admin),
    path('admin/forgot-password', vu.ForgotPassword.as_view()),
    path('forgot-password', vu.ForgotPassword.as_view()),
    re_path(r'client-config', vu.ClientConfiguration.as_view()),
    re_path(r'bot-properties$', vu.BotProperties.as_view()),
    re_path(r'client-form', vu.ClientForm.as_view()),
    re_path(r'analytics/(?P<slug>[\w-]+)', vu.Analytics.as_view()),
    re_path(r'assets/(?P<slug>[\w-]+)', vu.AssetsUploader.as_view()),
    re_path(r'(?P<slug>[\w-]+)/login', vu.Login.as_view()),
    re_path(r'(?P<slug>[\w-]+)/logout', vu.Logout.as_view()),
    path('customer/signup', vu.ClientSignup.as_view()),
    path('change-password', vu.ChangePassword.as_view()),
]
