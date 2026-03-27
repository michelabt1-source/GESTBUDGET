from django.shortcuts import render
from django.db.models import Sum, F
from .models import AllocationBudget, Depense

def analyse_budgetaire(request):
    # --- 1. LES CHIFFRES GLOBAUX (KPI) ---
    # Total du budget initial prévu (Allocation)
    total_alloue = AllocationBudget.objects.aggregate(Sum('budget_primitive'))['budget_primitive__sum'] or 0
    
    # Total des dépenses effectuées (Réalisations)
    total_depense = Depense.objects.aggregate(Sum('budget_primitive'))['budget_primitive__sum'] or 0
    
    # Prise en compte des modifications budgétaires (DBM)
    total_ajouts = AllocationBudget.objects.aggregate(Sum('dbm_ajout'))['dbm_ajout__sum'] or 0
    total_retraits = AllocationBudget.objects.aggregate(Sum('dbm_moins'))['dbm_moins__sum'] or 0
    
    # Budget Actuel Révisé = Initial + Ajouts - Retraits
    budget_revise = total_alloue + total_ajouts - total_retraits
    
    # Solde Disponible (Ce qu'il reste en caisse)
    solde_disponible = budget_revise - total_depense
    
    # Taux d'Exécution (Performance)
    taux_execution = (total_depense / budget_revise * 100) if budget_revise > 0 else 0

    # --- 2. ANALYSE PAR SECTION (TOP 5) ---
    # Quels sont les comptes qui consomment le plus ?
    top_depenses = Depense.objects.values('libelle_sous_compte', 'comptes') \
        .annotate(total=Sum('budget_primitive')) \
        .order_by('-total')[:5]

    context = {
        'total_alloue': total_alloue,
        'total_depense': total_depense,
        'budget_revise': budget_revise,
        'solde_disponible': solde_disponible,
        'taux_execution': round(taux_execution, 2),
        'top_depenses': top_depenses,
        'total_ajouts': total_ajouts,
        'total_retraits': total_retraits,
    }

    return render(request, 'budget_app/stats.html', context)