from django.db import models
from django.contrib.auth.models import AbstractUser
class Produit(models.Model):
    compte = models.CharField(max_length=100, verbose_name="Compte")
    designation = models.CharField(max_length=255, verbose_name="Désignation")
    quantite = models.FloatField(default=0, verbose_name="Quantité")
    unite = models.CharField(max_length=50, blank=True, null=True, verbose_name="Unité")
    specification = models.TextField(blank=True, null=True, verbose_name="Spécification")
    observation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Observation")

    def __str__(self):
        return f"{self.compte} - {self.designation}"
class Fournisseur(models.Model):
    code_four = models.CharField(max_length=50, unique=True, verbose_name="Code Fournisseur")
    nom = models.CharField(max_length=100, verbose_name="Nom/Raison Sociale")
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    ville = models.CharField(max_length=50, blank=True, null=True)
    nif_ou_compte = models.CharField(max_length=50, blank=True, null=True, verbose_name="N° Compte Bancaire")
    montant_engage = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.code_four} - {self.nom}"

class AllocationBudget(models.Model):
    num_compte_principal = models.CharField(max_length=50, verbose_name="N° Compte Principale")
    num_sous_compte = models.CharField(max_length=50, verbose_name="N° Sous Compte")
    nom_attache = models.CharField(max_length=100, verbose_name="Attaché")
    sous_compte = models.ForeignKey('SousCompte', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Sous-Compte")
    annee_ex = models.CharField(max_length=50, verbose_name="Année_EX")
    budget_primitive = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    libelle_sous_compte = models.CharField(max_length=255, verbose_name="Libellé")
    budget_mensuel = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    realisation_budget = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    mois = models.CharField(max_length=50, verbose_name="Mois")
    dbm_moins = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="DBM_Moins")
    dbm_ajout = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="DBM_Ajout")

    def __str__(self):
        if self.sous_compte:
            return f"{self.sous_compte} - {self.mois}"
        return f"Allocation {self.id} - {self.mois}"

class Budget(models.Model):
    allocation = models.ForeignKey(AllocationBudget, on_delete=models.CASCADE, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX")
    compte = models.CharField(max_length=50, verbose_name="Comptes") # Gardé 'compte' pour ton admin
    libelle_compte = models.CharField(max_length=255, verbose_name="Libellé_compte")
    
    # Montants (Noms alignés avec ton admin actuel)
    prevision = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    montant_engage = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    montant_realise = models.DecimalField(max_digits=18, decimal_places=2, default=0)    
    # Ajouts pour les futurs calculs (Recettes/Paiements)
    quantite_recette = models.FloatField(default=0)
    # Ce champ sera lié aux "DetailsPayement"
    montant_paye = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Cumul Paiements")
    # Ce champ sera lié aux "DetailsDepense" (Engagements)
    montant_engage = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Total Engagé")
    # Le résultat calculé
    reliquat = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Reliquat Disponible")
    def __str__(self):
        return self.libelle_compte

class Depense(models.Model):
    # --- Champs Texte (CharField) ---
    num_compte_principal = models.CharField(max_length=50, default="") 
    num_sous_compte = models.CharField(max_length=50, default="")
    nom_attache = models.CharField(max_length=50, verbose_name="Attaché", default="")
    comptes = models.CharField(max_length=50, default="")
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    libelle_sous_compte = models.CharField(max_length=50, verbose_name="Libellé", default="")
    fournisseur = models.CharField(max_length=50, default="Non spécifié")
    mois = models.CharField(max_length=50, default="")

    # --- Champs Numériques (DecimalField) -> Toujours mettre default=0 ---
    budget_primitive = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    budget_mensuel = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    realisation_budget = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dbm_moins = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dbm_ajout = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    # --- Champs Date ---
    # On ajoute null=True et blank=True pour éviter le blocage si la date est vide
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Dépense {self.id} - {self.annee_ex}"

class DetailsDepense(models.Model):
    depense_parente = models.ForeignKey(Depense, on_delete=models.CASCADE, verbose_name="IDDépenses")
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")
    
    code_four = models.CharField(max_length=50, default="") 
    date_depense = models.DateField(verbose_name="Date", null=True, blank=True)
    num_depense = models.CharField(max_length=50, verbose_name="Numero", default="")
    montant_depense = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_engagement = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    reliquat = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dbm_ajout = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dbm_moins = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    
    compte = models.CharField(max_length=50, default="")
    objet_depense = models.TextField(verbose_name="Objet", default="")
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")

    def __str__(self):
        return f"Détail {self.num_depense} - {self.montant_depense}"

class Paiement(models.Model):
    num_paiement = models.IntegerField(verbose_name="N° Ordre payment", default=0)
    date_payement = models.DateField(verbose_name="Date_pay", null=True, blank=True)
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    objet_payement = models.CharField(max_length=50, verbose_name="Objet", default="")
    valider_pay = models.BooleanField(default=False, verbose_name="Valider")

    def __str__(self):
        return f"Paiement {self.num_paiement}"
    
class DetailsPayement(models.Model):
    paiement_parent = models.ForeignKey(Paiement, on_delete=models.CASCADE, verbose_name="IDPayement1")
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")
    
    num_bon_engagement = models.IntegerField(verbose_name="N°", default=0)
    comptes = models.CharField(max_length=50, default="")
    fournisseur = models.CharField(max_length=50, default="")
    date_fact = models.DateField(verbose_name="Date Facture", null=True, blank=True)
    nom_service = models.CharField(max_length=50, verbose_name="Service", default="")
    montant_inscrit = models.CharField(max_length=50, verbose_name="MontantInscrit", default="")

class Recette(models.Model):
    num_recette = models.IntegerField(verbose_name="N°Recette", default=0)
    date_recette = models.DateField(verbose_name="Date", null=True, blank=True)
    montant_recette = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant", default=0)
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    valide = models.BooleanField(default=False, verbose_name="Validé")
    nom_totalisateur = models.CharField(max_length=50, verbose_name="Totalisateur", default="")
    nom_service = models.CharField(max_length=50, verbose_name="Service demandeur", default="")

    def __str__(self):
        return f"Recette {self.num_recette}"
    
class DetailsRecette(models.Model):
    recette_parente = models.ForeignKey(Recette, on_delete=models.CASCADE, verbose_name="IDRecette")
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")
    
    designation = models.CharField(max_length=50, verbose_name="Désignation", default="")
    quantite_recette = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Quantité", default=0)
    unite = models.CharField(max_length=50, verbose_name="Unité", default="")
    prix_unitaire_ht = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Prix Unitaire HT", default=0)
    prix_unitaire_ttc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Prix Unitaire TTC", default=0)
    nomenclature = models.CharField(max_length=50, verbose_name="Compte", default="")
    source = models.CharField(max_length=50, verbose_name="Source", default="")
    montant_ttc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant TTC", default=0)
    reference_pieces = models.CharField(max_length=50, verbose_name="Référence_pièces", default="")
    ipm = models.CharField(max_length=50, verbose_name="IPM", default="")
    code_recette = models.CharField(max_length=50, verbose_name="Type de recette", default="")
    nom_ipm = models.CharField(max_length=50, verbose_name="Nom_IPM", default="")

# --- ENGAGEMENTS (Bons & Détails) ---

class BonEngagement(models.Model):
    num_bon_engagement = models.IntegerField(verbose_name="N°", default=0)
    reference_pieces = models.CharField(max_length=50, verbose_name="Référence pièces", default="")
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    fournisseur = models.CharField(max_length=50, verbose_name="Fournisseur", default="")
    date_engagement = models.DateField(verbose_name="Date Engagement", null=True, blank=True)
    objet_engagement = models.CharField(max_length=50, verbose_name="Objet_Engagement", default="")
    nom_totalisateur = models.CharField(max_length=50, verbose_name="Totalisateur", default="")
    comptes = models.CharField(max_length=50, verbose_name="Comptes", default="")
    nombre_articles = models.IntegerField(verbose_name="Nombre articles", default=0)
    montant_engagement = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant engagement", default=0)
    montant_inscrit = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant inscrit", default=0)
    nom_service = models.CharField(max_length=50, verbose_name="Service demandeur", default="")
    
    # Type Interrupteur WinDev -> BooleanField
    facture = models.BooleanField(default=False, verbose_name="Facturé")
    valide = models.BooleanField(default=False, verbose_name="Validé")

    def __str__(self):
        return f"BE N°{self.num_bon_engagement} - {self.fournisseur}"

class DetailsEngagement(models.Model):
    # Liaisons
    bon_parent = models.ForeignKey(BonEngagement, on_delete=models.CASCADE, verbose_name="IDBonEngagement")
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")
    
    designation = models.CharField(max_length=50, verbose_name="Désignation", default="")
    specification = models.CharField(max_length=50, verbose_name="Spécification", default="")
    quantite_engagement = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Quantité", default=0)
    unite = models.CharField(max_length=50, verbose_name="Unité", default="")
    prix_unitaire_ht = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Prix Unitaire HT", default=0)
    prix_unitaire_ttc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Prix Unitaire TTC", default=0)
    montant_ttc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant TTC", default=0)
    observation = models.CharField(max_length=50, verbose_name="Observation", default="")
    compte = models.CharField(max_length=50, verbose_name="Compte", default="")

    def __str__(self):
        return f"Détail BE - {self.designation} ({self.montant_ttc})"
    
class SituationGeneralBugdet(models.Model):
    # Liaison avec le Budget (IDbudget dans HFSQL)
    budget_ligne = models.ForeignKey('Budget', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="IDbudget")

    # Champs Texte
    comptes = models.CharField(max_length=50, default="")
    annee_ex = models.CharField(max_length=50, verbose_name="Année_EX", default="")
    comptes_annee_ex = models.CharField(max_length=50, verbose_name="Comptes + Année_EX", default="") # Clé composée
    libelle_sous_compte = models.CharField(max_length=50, verbose_name="Libellé", default="")
    mois = models.CharField(max_length=50, default="")
    sigle = models.CharField(max_length=50, default="")
    service = models.CharField(max_length=50, default="")
    ville = models.CharField(max_length=50, default="")

    # Champs Numériques (Calculs)
    budget_primitive = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    budget_mensuel = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    realisation_budget = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dbm_moins = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dbm_ajout = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    
    # Indicateurs spécifiques à la Situation Générale
    taux_excurtion = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Taux exécution")
    reste_a = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Reste à")
    disponible = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Disponible")

    def __str__(self):
        return f"Situation {self.comptes} - {self.annee_ex}"

    class Meta:
        verbose_name = "Situation Générale Budget"
        verbose_name_plural = "Situations Générales Budget"

# --- FACTURATION ---

class Facture(models.Model):
    num_facture = models.IntegerField(verbose_name="N° Facture", default=0)
    date_fact = models.DateField(verbose_name="Date Facture", null=True, blank=True)
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    date_livraison = models.DateField(verbose_name="Date_livraison", null=True, blank=True)
    num_bon_livraison = models.IntegerField(verbose_name="N° Bon_Livraison", default=0)
    fournisseur = models.CharField(max_length=50, verbose_name="Fournisseur", default="")
    num_pvr = models.IntegerField(verbose_name="N°PV", default=0)
    montant_facture = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant Facture", default=0)
    quantite_facture = models.IntegerField(verbose_name="Nombre d'articles", default=0)
    
    # Interrupteurs WinDev
    validé = models.BooleanField(default=False, verbose_name="Engagé")
    payé = models.BooleanField(default=False, verbose_name="Payé")

    def __str__(self):
        return f"Facture {self.num_facture} - {self.fournisseur}"

class DetailsFacture(models.Model):
    # Liaisons
    facture_parente = models.ForeignKey(Facture, on_delete=models.CASCADE, verbose_name="IDFacture")
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")
    
    num_bon_engagement = models.IntegerField(verbose_name="N°", default=0)
    date_bc = models.DateField(verbose_name="Date de commande", null=True, blank=True)
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    fournisseur = models.CharField(max_length=50, default="")
    code_ser = models.CharField(max_length=50, verbose_name="Service", default="")
    objet_depense = models.CharField(max_length=50, verbose_name="Objet", default="")
    destinataire_bc = models.CharField(max_length=50, verbose_name="Destinataire", default="")
    totalisateur = models.CharField(max_length=50, default="")
    quantite_facture = models.IntegerField(verbose_name="Nombre d'articles", default=0)
    montant = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return f"Détail Facture - {self.objet_depense}"
    
# --- RÉCEPTIONS TECHNIQUES ---

class Technique(models.Model):
    num_pv_reception = models.IntegerField(verbose_name="N° PV Réception", default=0)
    date_reception = models.DateField(verbose_name="Date de Réception", null=True, blank=True)
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    fournisseur = models.CharField(max_length=50, verbose_name="Fournisseur", default="")
    validé = models.BooleanField(default=False, verbose_name="Validé")

    def __str__(self):
        return f"PV Reception {self.num_pv_reception} - {self.fournisseur}"

class DetailsTechnique(models.Model):
    # Liaisons
    technique_parent = models.ForeignKey(Technique, on_delete=models.CASCADE, verbose_name="IDTechnique1")
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")
    
    num_facture = models.IntegerField(verbose_name="N° Facture", default=0)
    date_fact = models.DateField(verbose_name="Date Facture", null=True, blank=True)
    quantite = models.IntegerField(verbose_name="Quantité", default=0)
    montant_fact = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant Fact", default=0)
    marche = models.CharField(max_length=50, verbose_name="Marché", default="")
    date_mar = models.DateField(verbose_name="Date Mar", null=True, blank=True)
    montant_pv = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant PV", default=0)
    commission = models.CharField(max_length=50, verbose_name="Commission", default="")

    def __str__(self):
        return f"Détail PV - Facture {self.num_facture}"

# --- RÉCEPTIONS ---

class Reception(models.Model):
    num_pv_reception = models.IntegerField(verbose_name="N° PV Réception", default=0)
    date_fact = models.DateField(verbose_name="Date Facture", null=True, blank=True)
    date_reception = models.DateField(verbose_name="Date de Réception", null=True, blank=True)
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    fournisseur = models.CharField(max_length=50, verbose_name="Fournisseur", default="")
    numero_facture = models.IntegerField(verbose_name="N° Facture", default=0)
    quantite = models.IntegerField(verbose_name="Quantité", default=0)
    montant_fact = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant_Fact", default=0)
    marche = models.CharField(max_length=50, verbose_name="Marché", default="")
    date_mar = models.DateField(verbose_name="Date Mar", null=True, blank=True)
    montant_pv = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant_PV", default=0)
    commission = models.CharField(max_length=50, verbose_name="Commission", default="")
    validé = models.BooleanField(default=False, verbose_name="Validé") # Interrupteur WinDev

    def __str__(self):
        return f"Réception PV {self.num_pv_reception} - {self.fournisseur}"

class DetailsReception(models.Model):
    # Liaisons
    reception_parente = models.ForeignKey(Reception, on_delete=models.CASCADE, verbose_name="IDRéception")
    budget_ligne = models.ForeignKey('Budget', on_delete=models.CASCADE, verbose_name="IDbudget")
    
    nomenclature = models.CharField(max_length=50, verbose_name="Compte", default="")
    designation = models.CharField(max_length=50, verbose_name="Désignation", default="")
    specification = models.CharField(max_length=50, verbose_name="Spécification", default="")
    quantite_reception = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Quantité", default=0)
    unite = models.CharField(max_length=50, verbose_name="Unité", default="")
    prix_unitaire_ht = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Prix Unitaire HT", default=0)
    prix_unitaire_ttc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Prix Unitaire TTC", default=0)
    montant_ttc = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant TTC", default=0)
    observation = models.CharField(max_length=50, verbose_name="Observation", default="")

    def __str__(self):
        return f"Détail Réception - {self.designation}"
    
# --- DÉCISIONS BUDGÉTAIRES MODIFICATIVES ---

class DBM(models.Model):
    budget_ligne = models.ForeignKey('Budget', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="IDbudget")
    
    date_dbm = models.DateField(verbose_name="Date DBM", null=True, blank=True)
    montant_dbm = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant DBM", default=0)
    comptes_de = models.CharField(max_length=50, verbose_name="Comptes d'origine", default="")
    compte_fi = models.CharField(max_length=50, verbose_name="Comptes destinataire", default="")
    annee_ex = models.CharField(max_length=50, verbose_name="Année_EX", default="")

    def __str__(self):
        return f"DBM {self.annee_ex} - {self.montant_dbm} ({self.comptes_de} -> {self.compte_fi})"

    class Meta:
        verbose_name = "DBM"
        verbose_name_plural = "DBMs"

# --- TABLES DE NOMENCLATURE ET PARAMÉTRAGE ---

class Chapitre(models.Model):
    code_chapitre = models.CharField(max_length=50, verbose_name="Code Chapitre", default="")
    libelle_chapitre = models.CharField(max_length=100, verbose_name="Libellé Chapitre", default="")

    def __str__(self):
        return f"{self.code_chapitre} - {self.libelle_chapitre}"

class IPM(models.Model):
    code_ipm = models.CharField(max_length=50, verbose_name="Code IPM", default="")
    libelle_ipm = models.CharField(max_length=100, verbose_name="Libellé IPM", default="")

    def __str__(self):
        return f"{self.code_ipm} - {self.libelle_ipm}"

class Mois(models.Model):
    nom_mois = models.CharField(max_length=50, verbose_name="Mois", default="")

    def __str__(self):
        return self.nom_mois
    class Meta:
        verbose_name_plural = "Mois"

class Unite(models.Model):
    libelle_unite = models.CharField(max_length=50, verbose_name="Unité", default="")

    def __str__(self):
        return self.libelle_unite
    
class Section(models.Model):
    num_section = models.IntegerField(verbose_name="N° Section", default=0)
    libelle_section = models.CharField(max_length=100, verbose_name="Libellé Section", default="")

    def __str__(self):
        return f"Section {self.num_section} : {self.libelle_section}"

class AnneeEnCours(models.Model):
    annee_ex = models.CharField(max_length=50, verbose_name="Code_EX", default="")
    valider = models.BooleanField(default=False, verbose_name="Année Active")

    def __str__(self):
        return self.annee_ex

class TypeBudget(models.Model):
    code_type = models.CharField(max_length=50, verbose_name="Code Type", default="")
    libelle_type = models.CharField(max_length=100, verbose_name="Libellé Type", default="")

    def __str__(self):
        return self.libelle_type
class NumComptePrincipal(models.Model):
    num_compte_principal = models.CharField(max_length=50, verbose_name="N° Compte Principal", default="")
    libelle_compte_principal = models.CharField(max_length=100, verbose_name="Libellé", default="")
    
    # Intégration des clés avec doublons (ForeignKeys)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Section", null=True, blank=True)
    type_budget = models.ForeignKey(TypeBudget, on_delete=models.CASCADE, verbose_name="Type de Budget", null=True, blank=True)

    def __str__(self):
        return f"{self.num_compte_principal} - {self.libelle_compte_principal}"
    
class SousCompte(models.Model):
    # Rubriques de base
    num_sous_compte = models.CharField(max_length=50, verbose_name="N° Sous-Compte", default="")
    libelle_sous_compte = models.CharField(max_length=100, verbose_name="Libellé Sous-Compte", default="")
    
    # Liaisons (Clés avec doublons WinDev)
    compte_principal = models.ForeignKey(
        'NumComptePrincipal', 
        on_delete=models.CASCADE, 
        verbose_name="Compte Principal", 
        null=True, 
        blank=True
    )
    
    annee_exercice = models.ForeignKey(
        'AnneeEnCours', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Année_EX"
    )
    
    # Ajout de la liaison avec l'Attaché
    attache = models.ForeignKey(
        'Attache', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Nom Attaché"
    )
    
    nom_type_compte = models.CharField(
        max_length=100, 
        verbose_name="Nom Type Compte", 
        default=""
    )

    def __str__(self):
        return f"{self.num_sous_compte} - {self.libelle_sous_compte}"
   
    
# --- TABLES DE RÉFÉRENCES SUPPLÉMENTAIRES ---

class Attache(models.Model):
    nom_attache = models.CharField(max_length=100, verbose_name="Nom Attaché", default="")

    def __str__(self):
        return self.nom_attache

class Services(models.Model):
    nom_service = models.CharField(max_length=100, verbose_name="Nom Service", default="")

    def __str__(self):
        return self.nom_service

class PlanComptable(models.Model):
    num_compte = models.CharField(max_length=50, verbose_name="N° Compte", default="")
    libelle_compte = models.CharField(max_length=150, verbose_name="Libellé Compte", default="")

    def __str__(self):
        return f"{self.num_compte} - {self.libelle_compte}"

class Cumul(models.Model):
    # Liaison possible avec SousCompte ou PlanComptable selon ta logique
    comptes = models.CharField(max_length=50, verbose_name="Comptes", default="")
    annee_ex = models.CharField(max_length=50, verbose_name="Année_EX", default="")
    
    # Montants de cumul
    montant_initial = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    montant_engage = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    montant_realise = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    montant_paye = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return f"Cumul {self.comptes} ({self.annee_ex})"
    
# --- SÉCURITÉ ET ACCÈS ---

class Role(models.Model):
    nom_role = models.CharField(max_length=100, verbose_name="Nom du Rôle", unique=True)

    def __str__(self):
        return self.nom_role

# On hérite de AbstractUser pour garder les fonctionnalités de base (email, username, etc.)
class Utilisateur(AbstractUser):
    # On ajoute la liaison avec ton modèle Role
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rôle")
    
    # On peut ajouter d'autres infos spécifiques ici
    service = models.CharField(max_length=100, verbose_name="Service / Direction", blank=True)

    def __str__(self):
        return self.username # AbstractUser utilise 'username' par défaut

# --- PARAMÉTRAGE COMPTABLE ---

class TypesDeComptes(models.Model):
    nom_type_compte = models.CharField(max_length=100, verbose_name="Type de Compte", default="")

    def __str__(self):
        return self.nom_type_compte

# --- FLUX ET ORGANISATION ---

class PeriodeRecette(models.Model):
    debut_periode_recette = models.DateField(verbose_name="Début Période", null=True, blank=True)
    fin_periode_recette = models.DateField(verbose_name="Fin Période", null=True, blank=True)
    compte = models.CharField(max_length=50, verbose_name="Compte", default="")
    code_recette = models.CharField(max_length=50, verbose_name="Code Recette", default="")

    def __str__(self):
        return f"Période {self.debut_periode_recette} au {self.fin_periode_recette}"

class Departement(models.Model):
    code_ser = models.CharField(max_length=50, verbose_name="Code Service", default="")
    nom_ser = models.CharField(max_length=100, verbose_name="Nom Service", default="")
    responsable_ser = models.CharField(max_length=100, verbose_name="Responsable", default="")
    
    # Interrupteurs WinDev
    recette = models.BooleanField(default=False, verbose_name="Recette")
    depense = models.BooleanField(default=False, verbose_name="Dépense")

    def __str__(self):
        return self.nom_ser

class Pay(models.Model):
    date_pay = models.DateField(verbose_name="Date Paiement", null=True, blank=True)
    montant_pay = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant", default=0)
    mode_pay = models.CharField(max_length=50, verbose_name="Mode de paiement", default="")
    objet_payement = models.CharField(max_length=200, verbose_name="Objet", default="")

    def __str__(self):
        return f"Pay {self.date_pay} - {self.montant_pay}"

class Source(models.Model):
    nom_source = models.CharField(max_length=100, verbose_name="Source de financement", default="")

    def __str__(self):
        return self.nom_source

class ExerciceBudgetaire(models.Model):
    annee_ex = models.CharField(max_length=50, verbose_name="Année Exercice", default="")

    def __str__(self):
        return self.annee_ex
    
# --- ANALYSE ET LOGISTIQUE ---

class Stock(models.Model):
    annee_exercice = models.ForeignKey('AnneeEnCours', on_delete=models.CASCADE, verbose_name="Année_EX")
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, verbose_name="Désignation")
    source = models.ForeignKey('Source', on_delete=models.CASCADE, verbose_name="Source")
    type_budget = models.ForeignKey('TypeBudget', on_delete=models.CASCADE, verbose_name="NomTypeBudget")

    reference = models.CharField(max_length=50, verbose_name="Référence", default="")
    unite = models.CharField(max_length=50, verbose_name="Unité", default="")
    quantite_stock = models.IntegerField(verbose_name="Quantité Stock", default=0)
    prix_unitaire_ttc = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    montant_stock = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return f"Stock {self.produit.designation} - {self.annee_exercice}"

class BudgetCompare(models.Model):
    compte_principal = models.ForeignKey('NumComptePrincipal', on_delete=models.CASCADE, verbose_name="NumComptePrincipal")
    
    comptes = models.CharField(max_length=50, verbose_name="Comptes", default="")
    libelle_sous_compte = models.CharField(max_length=150, verbose_name="Libellé", default="")
    annee_ex = models.CharField(max_length=50, verbose_name="Année_EX", default="")
    
     
    budget_primitive = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dbm_ajout = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dbm_moins = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    realisation_budget = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    reliquat = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return f"Comparaison {self.comptes} ({self.annee_ex})"
    
# --- CONTRÔLE ET PILOTAGE MENSUEL ---

class FicheControle(models.Model):
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, verbose_name="Fournisseur")
    
    num_fiche = models.IntegerField(verbose_name="N° Fiche", default=0)
    date_fiche = models.DateField(verbose_name="Date Fiche", null=True, blank=True)
    objet_fiche = models.CharField(max_length=200, verbose_name="Objet", default="")
    montant_fiche = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant", default=0)
    annee_ex = models.CharField(max_length=50, verbose_name="Année_EX", default="")
    valider = models.BooleanField(default=False, verbose_name="Validé")

    def __str__(self):
        return f"Fiche {self.num_fiche} - {self.fournisseur}"

class BudgetMensuel(models.Model):
    # Liaisons (Clés étrangères précisées)
    mois = models.ForeignKey('Mois', on_delete=models.CASCADE, verbose_name="Mois")
    # "Comptes" correspond généralement à SousCompte ou PlanComptable selon ton flux
    compte_budget = models.ForeignKey('SousCompte', on_delete=models.CASCADE, verbose_name="Comptes")
    annee_exercice = models.ForeignKey('AnneeEnCours', on_delete=models.CASCADE, verbose_name="Année_EX")
    
    # Montants mensuels
    montant_prevu = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant Prévu", default=0)
    montant_reel = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Montant Réel", default=0)
    ecart = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Écart", default=0)

    def __str__(self):
        return f"Budget {self.mois} - {self.compte_budget.num_sous_compte} ({self.annee_exercice})"
    
# --- RÈGLEMENTS ET COMMISSIONS ---

class ModeReglement(models.Model):
    mode_pay = models.CharField(max_length=100, verbose_name="Mode de paiement", default="")

    def __str__(self):
        return self.mode_pay

class MembresCommission(models.Model):
    nom_membre_commission = models.CharField(max_length=150, verbose_name="Nom du Membre", default="")
    qualite = models.CharField(max_length=100, verbose_name="Qualité / Titre", default="")
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True, verbose_name="Signature")

    def __str__(self):
        return f"{self.nom_membre_commission} ({self.qualite})"    