from datetime import date

from django import forms
from .models import DBM, AllocationBudget, BonEngagement, DetailsEngagement, Facture, SousCompte

class AllocationForm(forms.ModelForm):
    # 1. On garde tes choix pour les mois et années
    MOIS_CHOICES = [
        ('Janvier', 'Janvier'), ('Février', 'Février'), ('Mars', 'Mars'),
        ('Avril', 'Avril'), ('Mai', 'Mai'), ('Juin', 'Juin'),
        ('Juillet', 'Juillet'), ('Août', 'Août'), ('Septembre', 'Septembre'),
        ('Octobre', 'Octobre'), ('Novembre', 'Novembre'), ('Décembre', 'Décembre'),
    ]
    ANNEE_CHOICES = [(str(r), str(r)) for r in range(2024, 2031)]

    # Redéfinition des champs avec le style Bootstrap
    annee_ex = forms.ChoiceField(
        choices=ANNEE_CHOICES, 
        label="Exercice",
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )
    mois = forms.ChoiceField(
        choices=MOIS_CHOICES, 
        label="Mois de référence",
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )

    class Meta:
        model = AllocationBudget
        # On ajoute les champs DBM pour correspondre à ta capture WinDev
        fields = ['sous_compte', 'annee_ex', 'mois', 'budget_primitive', 'dbm_ajout', 'dbm_moins']
        
        widgets = {
            'sous_compte': forms.Select(attrs={
                'class': 'form-select fw-bold border-primary',
            }),
            'budget_primitive': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg fw-bold', 
                'placeholder': '0',
                'style': 'color: #0d6efd;' # Bleu pour le primitif
            }),
            'dbm_ajout': forms.NumberInput(attrs={
                'class': 'form-control border-success-subtle', 
                'placeholder': 'Ajout (+)',
                'style': 'background-color: #f8fff9; color: #198754;' # Fond vert léger
            }),
            'dbm_moins': forms.NumberInput(attrs={
                'class': 'form-control border-danger-subtle', 
                'placeholder': 'Retrait (-)',
                'style': 'background-color: #fff8f8; color: #dc3545;' # Fond rouge léger
            }),
            'annee_ex': forms.Select(attrs={
                'class': 'form-select border-primary-subtle',
            }),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On force l'affichage du libellé complet dans le menu déroulant
        self.fields['sous_compte'].empty_label = "--- Sélectionner un compte ---"

class DBMForm(forms.ModelForm):
    ANNEE_CHOICES = [(str(r), str(r)) for r in range(2024, 2031)]
    annee_ex = forms.ChoiceField(
        choices=ANNEE_CHOICES,
        label="Année Exercice",
        widget=forms.Select(attrs={'class': 'form-select border-primary-subtle'})
    )

    class Meta:
        model = DBM
        fields = ['compte_source', 'compte_destinataire', 'montant_dbm', 'date_dbm', 'annee_ex']
        widgets = {
            'compte_source': forms.Select(attrs={'class': 'form-select form-select-sm select2'}),
            'compte_destinataire': forms.Select(attrs={'class': 'form-select form-select-sm select2'}),
            'montant_dbm': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'date_dbm': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['annee_ex'].initial = str(date.today().year)

class BonEngagementForm(forms.ModelForm):
    class Meta:
        model = BonEngagement
        exclude = ['nombre_articles', 'montant_engagement', 'montant_inscrit']
        widgets = {
            'num_bon_engagement': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm fw-bold text-primary bg-light',
                'readonly': 'readonly',
                'placeholder': 'Auto'
            }),
            'date_engagement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'fournisseur': forms.Select(attrs={'class': 'form-select form-select-sm select2'}),
            'comptes': forms.Select(attrs={'class': 'form-select form-select-sm select2'}),
            'annee_ex': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly'}),
            'reference_pieces': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'objet_engagement': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '2'}),
            'nom_service': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'nom_totalisateur': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'valide': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # ✅ INDENTÉ CORRECTEMENT à l'intérieur de la classe
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num_bon_engagement'].required = False
class DetailsEngagementForm(forms.ModelForm):
    class Meta:
        model = DetailsEngagement
        fields = [
            'compte', 'designation', 'specification', 
            'quantite_engagement', 'prix_unitaire_ht', 
            'prix_unitaire_ttc', 'observation'
        ]
        widgets = {
            # On s'assure qu'ils ont la classe form-control pour être modifiables
            'compte': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Compte'}),
            'designation': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Article'}),
            'specification': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Spec.'}),
            'observation': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Obs.'}),
            'quantite_engagement': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-center', 'placeholder': '0', 'step': '0.01'}),
            'prix_unitaire_ht': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end', 'placeholder': '0', 'step': '0.01'}),
            'prix_unitaire_ttc': forms.NumberInput(attrs={'class': 'form-control form-control-sm text-end', 'placeholder': '0', 'step': '0.01'}),
        }
class FactureForm(forms.ModelForm):
    # Champ pour choisir l'engagement source (uniquement ceux validés)
    engagement_source = forms.ModelChoiceField(
        queryset=BonEngagement.objects.filter(valide=True),
        required=False,
        label="Lier à un Bon d'Engagement",
        widget=forms.Select(attrs={'class': 'form-select select2'})
    )

    class Meta:
        model = Facture
        fields = '__all__'
        exclude = ['validé', 'payé'] # On laisse la validation à une vue spécifique
        widgets = {
            'date_fact': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_livraison': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # ... autres widgets
        }
