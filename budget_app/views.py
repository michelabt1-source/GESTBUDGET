import json
from django import forms
from django.db.models.manager import BaseManager
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from budget_app.forms import AllocationForm, DBMForm
from budget_app.models import DBM, AllocationBudget, Fournisseur, MembresCommission, NumComptePrincipal, Produit, SousCompte, Unite, SituationGeneralBugdet

@login_required
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
@login_required
def structure_view(request):
    # 1. Récupérer le mot-clé tapé par l'utilisateur
    query = request.GET.get('q')
    
    # 2. Filtrer les produits si une recherche est lancée
    if query:
        produits_list = Produit.objects.filter(designation__icontains=query).order_by('designation')
    else:
        produits_list = Produit.objects.all().order_by('designation')
    context = {
        
        'produits': Produit.objects.all(),
        'fournisseurs': Fournisseur.objects.all(),
        'unites': Unite.objects.all(),
        'commissions': MembresCommission.objects.all(),
    }
    return render(request, 'budget_app/structure.html', context)
@login_required 
def index(request):
    return render(request, 'budget_app/index.html')

@login_required
def budget_view(request):
    # --- LOGIQUE D'ENREGISTREMENT (POST) ---
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget')

    # --- LOGIQUE D'AFFICHAGE (GET) ---
    comptes_principaux = NumComptePrincipal.objects.all().order_by('num_compte_principal')
    sous_comptes = SousCompte.objects.all().order_by('num_sous_compte')
    allocations = AllocationBudget.objects.all().order_by('sous_compte__num_sous_compte')
    historique_dbm = DBM.objects.all().order_by('-date_dbm')
    
    # Formulaire vide pour la modale
    form_allocation = AllocationForm()
    
    # Gestion des situations
    situations = SituationGeneralBugdet.objects.all()
    mois_select = request.GET.get('mois')
    if mois_select:
        situations = situations.filter(mois__iexact=mois_select)
    
    for s in situations:
        definitif = s.budget_primitive + s.dbm_ajout - s.dbm_moins
        s.disponible = definitif - s.realisation_budget
        s.taux_excurtion = round((s.realisation_budget / definitif) * 100, 2) if definitif > 0 else 0

    for a in allocations:
        a.budget_definitif = a.budget_primitive + a.dbm_ajout - a.dbm_moins

    context = {
        'comptes_principaux': comptes_principaux,
        'sous_comptes': sous_comptes,
        'allocations': allocations,
        'historique_dbm': historique_dbm,
        'situations': situations,
        'mois_select': mois_select,
        'form_allocation': form_allocation,
    }
    return render(request, 'budget_app/budget.html', context)

@login_required
def allocation_edit(request, pk):
    allocation = get_object_or_404(AllocationBudget, pk=pk)

    if request.method == 'POST':
        form = AllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            return redirect('budget_page')
    else:
        form = AllocationForm(instance=allocation)

    return render(request, 'budget_app/allocation_form.html', {
        'form': form,
        'allocation': allocation,
    })

@login_required
def allocation_delete(request, pk):
    allocation = get_object_or_404(AllocationBudget, pk=pk)

    if request.method == 'POST':
        allocation.delete()
        return redirect('budget_page')

    return render(request, 'budget_app/allocation_confirm_delete.html', {
        'allocation': allocation,
    })
def ajouter_dbm(request):
    if request.method == 'POST':
        form = DBMForm(request.POST)
        if form.is_valid():
            form.save() # Ici, le calcul dbm_moins / dbm_ajout se déclenche tout seul !
            return redirect('liste_dbm') # Remplacez par le nom de votre URL de liste
    else:
        form = DBMForm()
    
    return render(request, 'budget_app/nouveau_dbm.html', {'form': form})

class DBMCreateView(CreateView):
    model = DBM
    form_class = DBMForm
    template_name = 'budget_app/dbm_form.html' # Le fichier que nous avons créé
    success_url = reverse_lazy('dbm_list') # Redirection après succès

class DBMListView(ListView):
    model = DBM
    template_name = 'budget_app/dbm_list.html'
    context_object_name = 'mouvements'
    ordering = ['-date_dbm']

class DBMDeleteView(DeleteView):
    model = DBM
    template_name = 'budget_app/dbm_confirm_delete.html'
    success_url = reverse_lazy('dbm_list')
