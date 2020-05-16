"""rummi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.urls import include
from rummiApp import views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', include('rummiApp.urls')),
    path('AdminRummi/usersAdmin/', admin.site.urls),
    path('AdminRummi/account/',  include('django.contrib.auth.urls')),
    path('login/', views.index, name="login"),
    path('register/', views.index, name="register"),
    path('logout/', LogoutView.as_view(template_name='player/account/logout.html'), name="logout"),
    path('account/reset-pass/', PasswordResetView.as_view(template_name='player/account/resetPass.html'), name="password_reset"),
    path('account/reset-pass/done/', PasswordResetDoneView.as_view(template_name='player/account/resetPassDone.html'), name="password_reset_done"),
    path('account/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='player/account/resetPassConfirm.html'), name="password_reset_confirm"),
    path('account/reset/done/', PasswordResetCompleteView.as_view(template_name='player/account/resetPassComplete.html'), name="password_reset_complete"),
]
