import json
from django.shortcuts import render

from budget_app.models import Fournisseur, MembresCommission, Produit, Unite


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