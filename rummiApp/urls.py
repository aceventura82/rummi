from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [

    # API
    path('API/app/fetch/', views.APIViews.getData, name='getDataApp'),
    path('joinGame/<str:code>/', views.joinGame, name='joinGame'),

    # Player Web
    path('', views.Player.index, name='index'),
    path('login/', views.Player.index, name='login'),
    path('gameInfo/<int:gameId>/', views.Player.gameInfo, name='gameInfo'),
    path('game/<int:gameId>/', views.Player.game, name='game'),
    path('testing/', views.testing, name='testing'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('reset-pass/', PasswordResetView.as_view(template_name='resetPass.html'), name="password_reset"),
    path('reset-pass/done/', PasswordResetDoneView.as_view(template_name='resetPassDone.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='resetPassConfirm.html'), name="password_reset_confirm"),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='resetPassComplete.html'), name="password_reset_complete"),

]
