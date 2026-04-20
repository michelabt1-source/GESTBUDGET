from django.urls import path
from . import views

urlpatterns = [
    # Pages générales
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('structure/', views.structure_view, name='structure_page'),

    # Budget & Allocations
    path('budget/', views.budget_view, name='budget_page'),
    path('budget/allocation/<int:pk>/edit/', views.allocation_edit, name='allocation_edit'),
    path('budget/allocation/<int:pk>/delete/', views.allocation_delete, name='allocation_delete'),

    # DBM
    path('dbm/', views.DBMListView.as_view(), name='dbm_list'),
    path('dbm/nouveau/', views.DBMCreateView.as_view(), name='dbm_create'),
    path('dbm/<int:pk>/supprimer/', views.DBMDeleteView.as_view(), name='dbm_delete'),

    # Bons d'Engagement
    path('engagements/', views.BonEngagementListView.as_view(), name='engagement_list'),
    path('engagements/nouveau/', views.engagement_create_view, name='engagement_create'),
    path('engagements/<int:pk>/valider/', views.engagement_validate, name='engagement_validate'),      # ✅ AJOUTÉ
    path('engagements/<int:pk>/devalider/', views.engagement_devalidate, name='engagement_devalidate'),
    path('engagements/<int:pk>/imprimer/', views.engagement_print, name='engagement_print'),
    path('engagements/<int:pk>/imprimer-commande/', views.engagement_print_commande, name='engagement_print_commande'),

    # API
    path('api/get-produit/<int:produit_id>/', views.get_produit_details, name='get_produit_details'),
    path('engagements/<int:pk>/modifier/', views.engagement_edit_view, name='engagement_edit'),
    path('factures/nouveau/', views.facture_create_view, name='facture_create'),
    path('operations/', views.operations_view, name='operations_page'),
]