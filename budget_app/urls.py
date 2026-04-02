from django.urls import path
from . import views     
urlpatterns = [
    path('', views.home, name='home'),  
    path('structure/', views.structure_view, name='structure_page'),
    path('budget/', views.budget_view, name='budget_page'),
    # Ajoutez d'autres URL pour les différentes vues de votre application
]