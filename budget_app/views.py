import json
from django.db.models.manager import BaseManager
from django.shortcuts import render

from budget_app.models import DBM, AllocationBudget, Fournisseur, MembresCommission, NumComptePrincipal, Produit, SousCompte, Unite, SituationGeneralBugdet


def home(request):
    # Simulation de données issues de tes modèles (BonEngagement et Facture)
    # Dans ton vrai code, utilise .aggregate(Sum('montant'))
    labels = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"]
    
    # On divise par 1 000 000 pour simplifier l'affichage
    engagements = [12.5, 18.2, 14.0, 25.8, 22.1, 30.5] # En Millions
    realisations = [10.2, 15.0, 13.8, 20.1, 19.5, 25.0] # En Millions

    context = {
        'graph_labels': json.dumps(labels),
        'graph_engagements': json.dumps(engagements),
        'graph_realisations': json.dumps(realisations),
        # ... tes autres KPIs ...
    }
    return render(request, 'budget_app/home.html', context)
def structure_view(request):
    context = {
        'produits': Produit.objects.all(),
        'fournisseurs': Fournisseur.objects.all(),
        'unites': Unite.objects.all(),
        'commissions': MembresCommission.objects.all(),
    }
    return render(request, 'budget_app/structure.html', context)

def budget_view(request):
    comptes_principaux = NumComptePrincipal.objects.all().order_by('num_compte_principal')
    sous_comptes = SousCompte.objects.all().order_by('num_sous_compte')
    allocations = AllocationBudget.objects.all().order_by('comptes')
    historique_dbm = DBM.objects.all().order_by('-date_dbm')
    
    # 1. On récupère toutes les situations
    situations = SituationGeneralBugdet.objects.all()
    
    # 2. Filtrage (On utilise __iexact pour éviter les erreurs Majuscules/Minuscules)
    mois_select = request.GET.get('mois')
    if mois_select:
        situations = situations.filter(mois__iexact=mois_select)
    
    # 3. Les calculs sont BIEN FAITS ici
    for s in situations:
        # Budget Définitif = Primitif + Ajouts - Retraits
        definitif = s.budget_primitive + s.dbm_ajout - s.dbm_moins
        s.disponible = definitif - s.realisation_budget
        
        if definitif > 0:
            # On arrondit à 2 décimales pour le propre
            s.taux_excurtion = round((s.realisation_budget / definitif) * 100, 2)
        else:
            s.taux_excurtion = 0

    for a in allocations:
        a.budget_definitif = a.budget_primitive + a.dbm_ajout - a.dbm_moins

    # 4. TRÈS IMPORTANT : Ajouter 'situations' et 'mois_select' ici
    context = {
        'comptes_principaux': comptes_principaux,
        'sous_comptes': sous_comptes,
        'allocations': allocations,
        'historique_dbm': historique_dbm,
        'situations': situations,  # <--- NE PAS OUBLIER
        'mois_select': mois_select, # Pour savoir quel mois est actif
    }
    return render(request, 'budget_app/budget.html', context)