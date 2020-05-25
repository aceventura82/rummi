from django.urls import path
from . import views

urlpatterns = [

    # testing paths
    path('', views.index, name='Index'),
    path('testing/', views.testing, name='Testing'),
    path('API/app/fetch/', views.APIViews.getData, name='getDataApp'),

]
