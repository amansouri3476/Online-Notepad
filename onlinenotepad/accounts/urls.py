"""notely URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('signup/', views.signup),
    path('note/add/', views.add_note),
    path('note/get/', views.get_note),
    path('note/update/', views.update_note),
    path('note/delete/', views.delete_note),
    path('folder/add/', views.add_folder),
    path('folder/get_all/', views.get_folder_list),
    path('folder/get_content/', views.get_folder_content),
    path('folder/delete/', views.delete_folder),
]
