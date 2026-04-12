from django.urls import path
from . import views     
urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.home, name='home'),  
    path('structure/', views.structure_view, name='structure_page'),
    path('budget/', views.budget_view, name='budget_page'),
    path('budget/allocation/<int:pk>/edit/', views.allocation_edit, name='allocation_edit'),
    path('budget/allocation/<int:pk>/delete/', views.allocation_delete, name='allocation_delete'),
    # Ajoutez d'autres URL pour les différentes vues de votre application
]