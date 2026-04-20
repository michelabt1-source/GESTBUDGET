import json
from django.contrib import messages
from django import forms
from django.db.models.manager import BaseManager
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from budget_app.forms import AllocationForm, DBMForm, BonEngagementForm, DetailsEngagementForm, FactureForm
from budget_app.models import DBM, AllocationBudget, Budget, Fournisseur, MembresCommission, NumComptePrincipal, Produit, SousCompte, Unite, SituationGeneralBugdet,BonEngagement, DetailsEngagement, Facture, DetailsFacture

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


@login_required
def engagement_create_view(request):
    EngagementDetailsFormSet = inlineformset_factory(
        BonEngagement,
        DetailsEngagement,
        form=DetailsEngagementForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = BonEngagementForm(request.POST)
        
        if form.is_valid():
            # On sauvegarde d'abord le bon SANS commit=False
            # pour obtenir une instance avec un PK
            bon = form.save()
            
            # CORRECTION : on lie le formset à l'instance SAUVEGARDÉE
            formset = EngagementDetailsFormSet(request.POST, instance=bon)
            
            if formset.is_valid():
                try:
                    with transaction.atomic():
                        formset.save()
                    return redirect('engagement_list')
                except Exception as e:
                    print(f"Erreur lors de l'enregistrement : {e}")
                    bon.delete()  # Annule le bon si les détails échouent
            else:
                print("ERREURS FORMSET:", formset.errors)
                print("ERREURS NON-FORM:", formset.non_form_errors())
                bon.delete()  # Annule le bon si le formset est invalide
        else:
            # Formset vide pour réafficher le formulaire avec les erreurs
            formset = EngagementDetailsFormSet()
            print("ERREURS FORMULAIRE:", form.errors)
    else:
        form = BonEngagementForm()
        formset = EngagementDetailsFormSet()

    tous_les_produits = Produit.objects.all()

    return render(request, 'budget_app/engagement_form.html', {
        'form': form,
        'formset': formset,
        'tous_les_produits': tous_les_produits,
    })
class BonEngagementListView(LoginRequiredMixin, ListView):
    model = BonEngagement
    template_name = 'budget_app/engagement_list.html'
    context_object_name = 'engagements'
    ordering = ['-date_engagement']
@login_required
def engagement_validate(request, pk):
    bon = get_object_or_404(BonEngagement, pk=pk)
    bon.valide = True
    bon.save()
    return redirect('engagement_list')

@login_required
def engagement_devalidate(request, pk):
    bon = get_object_or_404(BonEngagement, pk=pk)
    bon.valide = False
    bon.save()
    return redirect('engagement_list')  
@login_required
def engagement_print(request, pk):
    bon = get_object_or_404(BonEngagement, pk=pk)
    details = bon.detailsengagement_set.all()
    return render(request, 'budget_app/engagement_print.html', {
        'bon': bon,
        'details': details,
    })  
@login_required
def engagement_print_commande(request, pk): 
    bon = get_object_or_404(BonEngagement, pk=pk)
    details = bon.detailsengagement_set.all()
    return render(request, 'budget_app/engagement_print_commande.html', {
        'bon': bon,
        'details': details,
    })
@login_required
def get_produit_details(request, produit_id):
    try:
        produit = Produit.objects.get(id=produit_id)
        data = {
            'designation': produit.designation,
            'specification': produit.specification,
            'unite': produit.unite.nom_unite if produit.unite else '',
        }
        return JsonResponse(data)
    except Produit.DoesNotExist:
        return JsonResponse({'error': 'Produit non trouvé'}, status=404)
@login_required
def engagement_edit_view(request, pk):
    bon = get_object_or_404(BonEngagement, pk=pk)
    
    EngagementDetailsFormSet = inlineformset_factory(
        BonEngagement,
        DetailsEngagement,
        form=DetailsEngagementForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = BonEngagementForm(request.POST, instance=bon)
        
        if form.is_valid():
            bon = form.save()
            formset = EngagementDetailsFormSet(request.POST, instance=bon)
            
            if formset.is_valid():
                try:
                    with transaction.atomic():
                        formset.save()
                    return redirect('engagement_list')
                except Exception as e:
                    print(f"Erreur : {e}")
            else:
                print("ERREURS FORMSET:", formset.errors)
        else:
            formset = EngagementDetailsFormSet(instance=bon)
            print("ERREURS FORM:", form.errors)
    else:
        form = BonEngagementForm(instance=bon)
        formset = EngagementDetailsFormSet(instance=bon)

    tous_les_produits = Produit.objects.all()

    return render(request, 'budget_app/engagement_form.html', {
        'form': form,
        'formset': formset,
        'tous_les_produits': tous_les_produits,
        'is_edit': True,  # ✅ Pour adapter le titre dans le template
    })
@login_required
def engagement_validate(request, pk):
    bon = get_object_or_404(BonEngagement, pk=pk)
    
    if bon.valide:
        messages.warning(request, "Ce bon est déjà validé.")
        return redirect('engagement_list')

    try:
        with transaction.atomic():
            details = bon.detailsengagement_set.all()
            
            for ligne in details:
                montant_ligne = (ligne.prix_unitaire_ttc or 0) * (ligne.quantite_engagement or 0)
                code_compte = ligne.compte 
    
                print(f"--- DEBUG VALIDATION ---")
                print(f"Compte cherché: '{code_compte}' | Année: '{bon.annee_ex}'")

                allocation = AllocationBudget.objects.filter(
                     num_sous_compte=code_compte, 
                     annee_ex=bon.annee_ex
               ).first()

                if allocation:
                   print(f"Allocation TROUVÉE : {allocation.id}")
                   allocation.realisation_budget += montant_ligne
                   allocation.save()
                else:
                   print(f"ERREUR : Allocation NON TROUVÉE pour le compte {code_compte}")

                # --- B. MISE À JOUR DU BUDGET GLOBAL (ANNUEL) ---
                budget_global = Budget.objects.filter(
                    compte=code_compte, 
                    annee_ex=bon.annee_ex
                ).first()

                if budget_global:
                    budget_global.montant_engage += montant_ligne
                    # On recalcule le reliquat immédiatement
                    budget_global.reliquat = budget_global.prevision - budget_global.montant_engage
                    budget_global.save()

                # --- C. MISE À JOUR DU FOURNISSEUR ---
                if bon.fournisseur:
                    # Si votre modèle Fournisseur a un champ cumulatif
                    # bon.fournisseur.montant_total_engage += montant_ligne
                    # bon.fournisseur.save()
                    pass

            # Finalisation : On marque le bon comme validé
            bon.valide = True
            bon.save()
            
            messages.success(request, f"Bon N°{bon.num_bon_engagement} validé. Budgets mis à jour.")

    except ValueError as e:
        messages.error(request, f"Alerte Budget : {str(e)}")
    except Exception as e:
        # CORRECTION ICI : Utilisez messages.error(request, ...) 
        # et non un dictionnaire
        messages.error(request, f"Erreur technique : {str(e)}")
        print(f"DEBUG: {str(e)}") # Pour voir l'erreur réelle dans votre console
    
    return redirect('engagement_list')
def facture_create_view(request):
    # On définit le formset pour les lignes de facture
    FactureDetailsFormSet = inlineformset_factory(
        Facture, 
        DetailsFacture,
        fields=('compte', 'designation', 'quantite_facture', 'prix_unitaire_ttc'),
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = FactureForm(request.POST) # Vous devrez créer FactureForm dans forms.py
        formset = FactureDetailsFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            facture = form.save()
            formset.instance = facture
            formset.save()
            return redirect('facture_list')
    else:
        form = FactureForm()
        formset = FactureDetailsFormSet()

    return render(request, 'budget_app/facture_form.html', {
        'form': form,
        'formset': formset
    })
def facture_create_view(request):
    FactureDetailsFormSet = inlineformset_factory(
    Facture, 
    DetailsFacture,
    # Utilisez UNIQUEMENT les noms de champs présents dans votre modèle ci-dessus
    fields=['objet_depense', 'quantite_facture', 'montant', 'fournisseur', 'annee_ex'],
    extra=1,
    can_delete=True,
    widgets={
        'objet_depense': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Désignation'}),
        'quantite_facture': forms.NumberInput(attrs={'class': 'form-control qty-fact'}),
        'montant': forms.NumberInput(attrs={'class': 'form-control pu-fact'}),
        'fournisseur': forms.HiddenInput(), # On peut les cacher si on les remplit par JS
        'annee_ex': forms.HiddenInput(),
    }
    )

    if request.method == 'POST':
        form = FactureForm(request.POST)
        formset = FactureDetailsFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            facture = form.save()
            formset.instance = facture
            formset.save()
            messages.success(request, f"Facture {facture.num_facture} enregistrée.")
            return redirect('facture_list')
    else:
        form = FactureForm()
        formset = FactureDetailsFormSet()

    return render(request, 'budget_app/facture_form.html', {
        'form': form,
        'formset': formset
    })

def get_engagement_details(request, engagement_id):
    try:
        bon = BonEngagement.objects.get(id=engagement_id)
        details = DetailsEngagement.objects.filter(bon_parent=bon)
        
        lignes = []
        for d in details:
            lignes.append({
                'compte': d.compte,
                'designation': d.designation,
                'quantite': float(d.quantite_engagement),
                'prix_ttc': float(d.prix_unitaire_ttc),
            })
            
        return JsonResponse({
            'fournisseur': bon.fournisseur.nom if bon.fournisseur else "",
            'annee': bon.annee_ex,
            'lignes': lignes
        })
    except BonEngagement.DoesNotExist:
        return JsonResponse({'error': 'Engagement non trouvé'}, status=404)
def operations_view(request):
    # Ici, vous pouvez récupérer et afficher les opérations récentes (DBM, engagements, factures)
    dbms_recents = DBM.objects.all().order_by('-date_dbm')[:10]
    engagements_recents = BonEngagement.objects.all().order_by('-date_engagement')[:10]
    factures_recents = Facture.objects.all().order_by('-date_fact')[:10]

    context = {
        'dbms_recents': dbms_recents,
        'engagements_recents': engagements_recents,
        'factures_recents': factures_recents,
    }
    return render(request, 'budget_app/operations.html', context)