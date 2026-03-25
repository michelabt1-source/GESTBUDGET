from django.contrib import admin
from .models import DBM, IPM, AllocationBudget, AnneeEnCours, Attache, BonEngagement, BudgetCompare, BudgetMensuel, Chapitre, Cumul, Departement, Depense, DetailsDepense, DetailsEngagement, DetailsFacture, DetailsPayement, DetailsReception, DetailsRecette, DetailsTechnique, ExerciceBudgetaire, Facture, FicheControle, Fournisseur, Budget, MembresCommission, ModeReglement, Mois, NumComptePrincipal, Paiement, Pay, PeriodeRecette, PlanComptable, Reception, Recette, Produit, Role, Section, Services, SituationGeneralBugdet, Source, SousCompte, Stock, Technique, TypeBudget, TypesDeComptes, Unite, Utilisateur

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('num_paiement', 'date_payement', 'annee_ex', 'objet_payement', 'valider_pay')
    list_filter = ('annee_ex', 'valider_pay')
    search_fields = ('num_paiement', 'objet_payement')

@admin.register(DetailsPayement)
class DetailsPayementAdmin(admin.ModelAdmin):
    list_display = ('num_bon_engagement', 'comptes', 'fournisseur', 'date_fact', 'budget_ligne')
    list_filter = ('date_fact', 'budget_ligne')

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('code_four', 'nom', 'telephone', 'ville', 'montant_engage')
    search_fields = ('nom', 'code_four')
    list_filter = ('ville',)

@admin.register(AllocationBudget)
class AllocationBudgetAdmin(admin.ModelAdmin):
    list_display = ('annee_ex', 'mois', 'comptes', 'budget_primitive')
    list_filter = ('annee_ex', 'mois')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
   
    list_display = ('annee_ex', 'compte', 'libelle_compte', 'reliquat')
    list_filter = ('annee_ex',)
    search_fields = ('compte', 'libelle_compte')    

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'annee_ex', 'comptes', 'realisation_budget')

@admin.register(DetailsDepense)
class DetailsDepenseAdmin(admin.ModelAdmin):
    list_display = ('num_depense', 'date_depense', 'montant_depense', 'budget_ligne')
    list_filter = ('annee_ex', 'budget_ligne')

@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
    list_display = ('num_recette', 'date_recette', 'montant_recette', 'valide')

@admin.register(DetailsRecette)
class DetailsRecetteAdmin(admin.ModelAdmin):
    list_display = ('designation', 'montant_ttc', 'budget_ligne')

@admin.register(BonEngagement)
class BonEngagementAdmin(admin.ModelAdmin):
    list_display = ('num_bon_engagement', 'fournisseur', 'date_engagement', 'montant_engagement', 'valide')
    list_filter = ('annee_ex', 'valide', 'facture')
    search_fields = ('num_bon_engagement', 'fournisseur', 'objet_engagement')

@admin.register(DetailsEngagement)
class DetailsEngagementAdmin(admin.ModelAdmin):
    list_display = ('designation', 'quantite_engagement', 'montant_ttc', 'budget_ligne')
    list_filter = ('budget_ligne',)

@admin.register(SituationGeneralBugdet)
class SituationGeneralBugdetAdmin(admin.ModelAdmin):
    list_display = ('comptes', 'annee_ex', 'budget_primitive', 'realisation_budget', 'disponible', 'taux_excurtion')
    list_filter = ('annee_ex', 'mois', 'service')
    search_fields = ('comptes', 'libelle_sous_compte')

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('num_facture', 'fournisseur', 'date_fact', 'montant_facture', 'payé')
    list_filter = ('annee_ex', 'payé', 'validé')
    search_fields = ('num_facture', 'fournisseur')

@admin.register(DetailsFacture)
class DetailsFactureAdmin(admin.ModelAdmin):
    list_display = ('objet_depense', 'montant', 'budget_ligne', 'facture_parente')
    list_filter = ('budget_ligne',)
@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ('num_pv_reception', 'fournisseur', 'date_reception', 'validé')
    list_filter = ('annee_ex', 'validé')
    search_fields = ('num_pv_reception', 'fournisseur')

@admin.register(DetailsTechnique)
class DetailsTechniqueAdmin(admin.ModelAdmin):
    list_display = ('num_facture', 'montant_pv', 'marche', 'budget_ligne')
    list_filter = ('budget_ligne',)

@admin.register(Reception)
class ReceptionAdmin(admin.ModelAdmin):
    list_display = ('num_pv_reception', 'fournisseur', 'date_reception', 'montant_pv', 'validé')
    list_filter = ('annee_ex', 'validé')
    search_fields = ('num_pv_reception', 'fournisseur', 'marche')

@admin.register(DetailsReception)
class DetailsReceptionAdmin(admin.ModelAdmin):
    list_display = ('designation', 'quantite_reception', 'montant_ttc', 'budget_ligne')
    list_filter = ('budget_ligne',)

@admin.register(DBM)
class DBMAdmin(admin.ModelAdmin):
    list_display = ('date_dbm', 'comptes_de', 'compte_fi', 'montant_dbm', 'annee_ex')
    list_filter = ('annee_ex', 'date_dbm')
    search_fields = ('comptes_de', 'compte_fi')

@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ('code_chapitre', 'libelle_chapitre')

@admin.register(IPM)
class IPMAdmin(admin.ModelAdmin):
    list_display = ('code_ipm', 'libelle_ipm')

@admin.register(Mois)
class MoisAdmin(admin.ModelAdmin):
    list_display = ('nom_mois',)

@admin.register(NumComptePrincipal)
class NumComptePrincipalAdmin(admin.ModelAdmin):
    list_display = ('num_compte_principal', 'libelle_compte_principal', 'section', 'type_budget')
    list_filter = ('section', 'type_budget') 
    search_fields = ('num_compte_principal', 'libelle_compte_principal')

@admin.register(SousCompte)
class SousCompteAdmin(admin.ModelAdmin):
    list_display = ('num_sous_compte', 'libelle_sous_compte', 'compte_principal', 'attache', 'annee_exercice')
    list_filter = ('annee_exercice', 'compte_principal', 'attache')
    search_fields = ('num_sous_compte', 'libelle_sous_compte')

@admin.register(Unite)
class UniteAdmin(admin.ModelAdmin):
    list_display = ('libelle_unite',)

@admin.register(AnneeEnCours)
class AnneeEnCoursAdmin(admin.ModelAdmin):
    list_display = ('annee_ex', 'valider')
    list_editable = ('valider',)  # Permet d'activer l'année directement dans la liste
    list_filter = ('valider',)
    search_fields = ('annee_ex',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('num_section', 'libelle_section')
    search_fields = ('num_section', 'libelle_section')
    ordering = ('num_section',)

@admin.register(TypeBudget)
class TypeBudgetAdmin(admin.ModelAdmin):
    list_display = ('code_type', 'libelle_type')
    search_fields = ('code_type', 'libelle_type')

@admin.register(Attache)
class AttacheAdmin(admin.ModelAdmin):
    list_display = ('nom_attache',)

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('nom_service',)

@admin.register(PlanComptable)
class PlanComptableAdmin(admin.ModelAdmin):
    list_display = ('num_compte', 'libelle_compte')
    search_fields = ('num_compte', 'libelle_compte')

@admin.register(Cumul)
class CumulAdmin(admin.ModelAdmin):
    list_display = ('comptes', 'annee_ex', 'montant_initial', 'montant_engage')
    list_filter = ('annee_ex',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('nom_role',)

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom_user', 'role')
    list_filter = ('role',)

@admin.register(TypesDeComptes)
class TypesDeComptesAdmin(admin.ModelAdmin):
    list_display = ('nom_type_compte',)

@admin.register(PeriodeRecette)
class PeriodeRecetteAdmin(admin.ModelAdmin):
    list_display = ('debut_periode_recette', 'fin_periode_recette', 'code_recette')

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('code_ser', 'nom_ser', 'responsable_ser', 'recette', 'depense')
    list_filter = ('recette', 'depense')

@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ('date_pay', 'montant_pay', 'mode_pay')
    search_fields = ('objet_payement',)

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('nom_source',)

@admin.register(ExerciceBudgetaire)
class ExerciceBudgetaireAdmin(admin.ModelAdmin):
    list_display = ('annee_ex',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'annee_exercice', 'quantite_stock', 'montant_stock', 'source')
    list_filter = ('annee_exercice', 'source', 'type_budget')
    search_fields = ('reference',)

@admin.register(BudgetCompare)
class BudgetCompareAdmin(admin.ModelAdmin):
    list_display = ('comptes', 'libelle_sous_compte', 'annee_ex', 'reliquat')
    list_filter = ('annee_ex', 'compte_principal')
    search_fields = ('comptes', 'libelle_sous_compte')

@admin.register(FicheControle)
class FicheControleAdmin(admin.ModelAdmin):
    list_display = ('num_fiche', 'fournisseur', 'date_fiche', 'montant_fiche', 'valider')
    list_filter = ('valider', 'annee_ex')
    search_fields = ('objet_fiche', 'fournisseur__nom_fournisseur')

@admin.register(BudgetMensuel)
class BudgetMensuelAdmin(admin.ModelAdmin):
    list_display = ('mois', 'compte_budget', 'annee_exercice', 'montant_prevu', 'montant_reel')
    list_filter = ('annee_exercice', 'mois')

@admin.register(ModeReglement)
class ModeReglementAdmin(admin.ModelAdmin):
    list_display = ('mode_pay',)

@admin.register(MembresCommission)
class MembresCommissionAdmin(admin.ModelAdmin):
    list_display = ('nom_membre_commission', 'qualite')
    search_fields = ('nom_membre_commission',)
# On définit d'abord comment on veut afficher les données
class ProduitAdmin(admin.ModelAdmin):
    # Les colonnes qui seront visibles dans la liste
    list_display = ('compte', 'designation', 'quantite', 'unite')
    # La barre de recherche pour fouiller dans tes 2892 produits
    search_fields = ('designation', 'compte')
    # Les filtres sur le côté droit
    list_filter = ('unite',)

# ENSUITE, on enregistre le modèle AVEC sa configuration
admin.site.register(Produit, ProduitAdmin)
