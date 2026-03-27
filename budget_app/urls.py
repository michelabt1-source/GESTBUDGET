from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.analyse_budgetaire, name='analyse_budgetaire'),
] 