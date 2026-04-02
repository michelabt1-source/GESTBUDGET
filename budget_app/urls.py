from django.urls import path
from . import views     
urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.home, name='home'),  
    path('structure/', views.structure_view, name='structure_page'),# Ajoutez d'autres URL pour les différentes vues de votre application
]