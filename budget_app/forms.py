from django import forms
from .models import DBM, AllocationBudget, SousCompte

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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On force l'affichage du libellé complet dans le menu déroulant
        self.fields['sous_compte'].empty_label = "--- Sélectionner un compte ---"

class DBMForm(forms.ModelForm):
    class Meta:
        model = DBM
        fields = ['compte_source', 'compte_destinataire', 'montant_dbm', 'date_dbm']
        widgets = {
            'compte_source': forms.Select(attrs={'class': 'form-select select2'}),
            'compte_destinataire': forms.Select(attrs={'class': 'form-select select2'}),
            'montant_dbm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_dbm': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
