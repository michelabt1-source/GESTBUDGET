import os
import django
import pandas as pd

# 1. Configurer la variable d'environnement AVANT setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJETGCS.settings')

# 2. Lancer setup
django.setup()

# 1. Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJETGCS.settings')
django.setup()

# 2. Import des modèles
from budget_app.models import Produit, MembresCommission, ModeReglement,IPM, Paiement, Facture, Fournisseur, DBM, Depense,Chapitre, BonEngagement, ExerciceBudgetaire,AllocationBudget,NumComptePrincipal, SousCompte, AnneeEnCours, Technique, TypeBudget, Utilisateur, Role
from decimal import Decimal
from datetime import datetime



def importer_technique():
    chemin = r'table windev/Table Technique.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                num_pv = row['N° PV Réception']
                if pd.notna(num_pv):
                    _, created = Technique.objects.get_or_create(
                        num_pv_reception=num_pv,
                        annee_ex=str(row['Code_EX']) if pd.notna(row['Code_EX']) else "2025",
                        fournisseur=row['Fournisseur'] if pd.notna(row['Fournisseur']) else "",
                        defaults={
                            'date_reception': row['Date de Réception'] if pd.notna(row['Date de Réception']) else None,
                            'validé': bool(row['Validé']) if pd.notna(row['Validé']) else False,
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Technique (PV Réception) : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Technique : {e}")

def importer_types_budget():
    chemin = r'table windev/Table typedeBudget.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                code = row['Type de budget']
                if pd.notna(code):
                    _, created = TypeBudget.objects.get_or_create(
                        code_type=code,
                        defaults={'libelle_type': row['Libellé_TB'] if pd.notna(row['Libellé_TB']) else code}
                    )
                    if created: compteur += 1
            print(f"✅ Types de Budget : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Types Budget : {e}")

def importer_utilisateurs():
    chemin = r'table windev/Table utilisateur.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                nom = str(row['Utilisateur']).strip() # On s'assure que c'est du texte propre
                role_nom = str(row['Role']).strip() if pd.notna(row['Role']) else "Utilisateur"
                mdp_brut = str(row['Mot de passe']) if pd.notna(row['Mot de passe']) else "1234"
                
                if pd.notna(nom) and nom != "":
                    # 1. Gestion du rôle
                    role_obj, _ = Role.objects.get_or_create(nom_role=role_nom)
                    
                    # 2. Vérification si l'utilisateur existe déjà via 'username'
                    user_obj, created = Utilisateur.objects.get_or_create(
                        username=nom,
                        defaults={
                            'role': role_obj,
                            'is_staff': True if role_nom.lower() == "administrateur" else False
                        }
                    )
                    
                    if created:
                        # 3. TRÈS IMPORTANT : Hachage du mot de passe
                        user_obj.set_password(mdp_brut)
                        user_obj.save()
                        compteur += 1
                        
            print(f"✅ Utilisateurs : {compteur} nouveaux ajoutés (avec mots de passe hachés).")
        except Exception as e:
            print(f"❌ Erreur Utilisateurs : {e}")
def importer_comptes_principaux():
    chemin = r'table windev/NumComptePrincipal.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                num = str(row['N° Compte Principale'])
                if pd.notna(num):
                    # Utilisation de libelle_compte_principal selon ton modèle
                    _, created = NumComptePrincipal.objects.get_or_create(
                        num_compte_principal=num,
                        defaults={
                            'libelle_compte_principal': row['Libellé'] if pd.notna(row['Libellé']) else ""
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Comptes Principaux : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Comptes Principaux : {e}")

def importer_sous_comptes():
    chemin = r'table windev/Table SousCompte.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                num_sc = str(row['Comptes'])
                annee_val = str(row['Code_EX']) if pd.notna(row['Code_EX']) else "2025"

                if pd.notna(num_sc):
                    # 1. On récupère l'année avec le bon nom de champ : annee_ex
                    annee_obj, _ = AnneeEnCours.objects.get_or_create(annee_ex=annee_val)
                    
                    # 2. On crée le Sous-Compte avec les bons noms de champs détectés
                    # On utilise num_sous_compte et annee_exercice (tes noms de ForeignKey)
                    _, created = SousCompte.objects.get_or_create(
                        num_sous_compte=num_sc,
                        annee_exercice=annee_obj, 
                        defaults={
                            'libelle_sous_compte': row['Libellé'] if pd.notna(row['Libellé']) else "",
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Sous-Comptes : {compteur} nouveaux ajoutés.")
        except Exception as e:
            # On affiche l'erreur précise ici
            print(f"❌ Erreur Sous-Comptes : {e}")
def importer_allocations():
    chemin = r'table windev/Table Allocation_budget.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                # On utilise 'num_sous_compte' au lieu de 'comptes'
                compte_val = str(row['Comptes']) if pd.notna(row['Comptes']) else ""
                annee_val = str(row['Code_EX']) if pd.notna(row['Code_EX']) else ""
                
                if compte_val and annee_val:
                    # Correction ici : 'num_sous_compte' doit être utilisé
                    _, created = AllocationBudget.objects.get_or_create(
                        num_sous_compte=compte_val, # Changé de 'comptes' à 'num_sous_compte'
                        annee_ex=annee_val,
                        libelle_sous_compte=row['Libellé'] if pd.notna(row['Libellé']) else "",
                        defaults={
                            'num_compte_principal': str(row['N° Compte Principale']) if pd.notna(row['N° Compte Principale']) else "",
                            'budget_primitive': Decimal(str(row['Budget_Primitive'])) if pd.notna(row['Budget_Primitive']) else 0,
                            'budget_mensuel': Decimal(str(row['Budget_Mensuel'])) if pd.notna(row['Budget_Mensuel']) else 0,
                            'realisation_budget': Decimal(str(row['Réalisation_Budget'])) if pd.notna(row['Réalisation_Budget']) else 0,
                            'dbm_moins': Decimal(str(row['DBM_Moins'])) if pd.notna(row['DBM_Moins']) else 0,
                            'dbm_ajout': Decimal(str(row['DBM_Ajout'])) if pd.notna(row['DBM_Ajout']) else 0,
                            'nom_attache': str(row['Num_attaché']) if pd.notna(row['Num_attaché']) else "",
                            'mois': "Janvier", 
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Allocations Budget : {compteur} nouvelles ajoutées.")
        except Exception as e:
            print(f"❌ Erreur Allocations : {e}")
    else:
        print(f"⚠️ Fichier introuvable : {chemin}")
def importer_chapitres():
    chemin = r'table windev/Table chapitre.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                code = row['Code_Chapitre']
                if pd.notna(code):
                    _, created = Chapitre.objects.get_or_create(
                        code_chapitre=code,
                        defaults={'libelle_chapitre': row['Libellé_Chapitre'] if pd.notna(row['Libellé_Chapitre']) else ""}
                    )
                    if created: compteur += 1
            print(f"✅ Chapitres : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Chapitres : {e}")

def importer_bons_engagement():
    chemin = r'table windev/Table BonEngagement.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                # On utilise N° (colonne Excel) pour num_bon_engagement (modèle)
                num_be = row['N°']
                if pd.notna(num_be):
                    _, created = BonEngagement.objects.get_or_create(
                        num_bon_engagement=num_be,
                        annee_ex=str(row['Code_EX']) if pd.notna(row['Code_EX']) else "2025",
                        defaults={
                            'reference_pieces': row['Référence_pièces'] if pd.notna(row['Référence_pièces']) else "",
                            'fournisseur': row['Fournisseur'] if pd.notna(row['Fournisseur']) else "",
                            'date_engagement': row['Date Engagement'] if pd.notna(row['Date Engagement']) else None,
                            'objet_engagement': row['Objet_Engagement'] if pd.notna(row['Objet_Engagement']) else "",
                            'nom_totalisateur': row['Totalisateur'] if pd.notna(row['Totalisateur']) else "",
                            'comptes': str(row['Comptes']) if pd.notna(row['Comptes']) else "",
                            'montant_inscrit': Decimal(str(row['Montant_inscrit'])) if pd.notna(row['Montant_inscrit']) else 0,
                            'nom_service': row['Service demandeur'] if pd.notna(row['Service demandeur']) else "",
                            'facture': bool(row['Facturé']) if pd.notna(row['Facturé']) else False,
                            'valide': bool(row['Validé']) if pd.notna(row['Validé']) else False,
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Bons d'Engagement : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Bons Engagement : {e}")

def importer_exercices():
    chemin = r'table windev/Table annéebudétaire.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                annee = str(row['Code_EX'])
                if pd.notna(annee):
                    _, created = ExerciceBudgetaire.objects.get_or_create(annee_ex=annee)
                    if created: compteur += 1
            print(f"✅ Exercices Budgétaires : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Exercices : {e}")
def importer_depenses():
    chemin = r'table windev/Table Dépenses.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                # On utilise le compte, le libellé et la date pour identifier une dépense unique
                compte_val = str(row['Comptes']) if pd.notna(row['Comptes']) else ""
                libelle_val = row['Libellé'] if pd.notna(row['Libellé']) else ""
                date_val = row['Date'] if pd.notna(row['Date']) else None
                
                if compte_val:
                    _, created = Depense.objects.get_or_create(
                        comptes=compte_val,
                        libelle_sous_compte=libelle_val,
                        date=date_val,
                        defaults={
                            'budget_primitive': Decimal(str(row['Budget_Primitive'])) if pd.notna(row['Budget_Primitive']) else 0,
                            'realisation_budget': Decimal(str(row['Réalisation_Budget'])) if pd.notna(row['Réalisation_Budget']) else 0,
                            # On extrait l'année de la date si possible
                            'annee_ex': str(date_val.year) if hasattr(date_val, 'year') else "2025",
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Dépenses : {compteur} nouvelles ajoutées.")
        except Exception as e:
            print(f"❌ Erreur Dépenses : {e}")

def importer_dbm():
    chemin = r'table windev/Table DBM.xlsx'
    if not os.path.exists(chemin):
        print(f"⚠️ Fichier introuvable : {chemin}")
        return

    def normalize_code(value):
        if pd.isna(value):
            return ""
        code = str(value).strip()
        if code.endswith(".0"):
            code = code[:-2]
        return code

    try:
        df = pd.read_excel(chemin)
        allocations = AllocationBudget.objects.all()
        allocations_by_sous = {
            str(a.num_sous_compte).strip(): a
            for a in allocations
            if a.num_sous_compte
        }
        allocations_by_principal = {
            str(a.num_compte_principal).strip(): a
            for a in allocations
            if a.num_compte_principal
        }

        compteur = 0
        skipped = 0

        for _, row in df.iterrows():
            date_d = row.get("Date_DBM") if pd.notna(row.get("Date_DBM")) else None
            montant = (
                Decimal(str(row["Montant_DBM"]))
                if pd.notna(row.get("Montant_DBM"))
                else Decimal("0")
            )

            source_code = normalize_code(row.get("Comptes d'origine"))
            dest_code = normalize_code(row.get("Comptes destinateur"))

            if not source_code or not dest_code:
                skipped += 1
                continue

            source = allocations_by_sous.get(source_code) or allocations_by_principal.get(source_code)
            dest = allocations_by_sous.get(dest_code) or allocations_by_principal.get(dest_code)

            if source is None or dest is None:
                skipped += 1
                continue

            _, created = DBM.objects.get_or_create(
                date_dbm=date_d,
                montant_dbm=montant,
                compte_source=source,
                compte_destinataire=dest,
                defaults={
                    "annee_ex": str(row.get("Année AnnéeCours")).strip()
                    if pd.notna(row.get("Année AnnéeCours"))
                    else "2025",
                },
            )
            if created:
                compteur += 1

        print(
            f"✅ DBM (Décisions Budgétaires Modificatives) : {compteur} nouvelles ajoutées."
            + (f" {skipped} lignes ignorées." if skipped else "")
        )
    except Exception as e:
        print(f"❌ Erreur DBM : {e}")
def importer_fournisseurs():
    chemin = r'table windev/Table Fournisseur.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                # On utilise 'Service demandeur' comme code unique (ex: ABBA, AFCOP)
                code = row['Service demandeur']
                if pd.notna(code):
                    _, created = Fournisseur.objects.get_or_create(
                        code_four=code,
                        defaults={
                            'nom': row['Fournisseur'] if pd.notna(row['Fournisseur']) else code,
                            'adresse': row['Adresse'] if pd.notna(row['Adresse']) else "",
                            'telephone': str(row['Téléphone']) if pd.notna(row['Téléphone']) else "",
                            'ville': row['Ville'] if pd.notna(row['Ville']) else "",
                            'nif_ou_compte': str(row['N°Compte bancaire']) if pd.notna(row['N°Compte bancaire']) else "",
                            'montant_engage': Decimal(str(row['Facturées Payés'])) if pd.notna(row['Facturées Payés']) else 0,
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Fournisseurs : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Fournisseurs : {e}")

def importer_factures():
    chemin = r'table windev/Table Facture.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                num_f = row['N° Facture']
                if pd.notna(num_f):
                    # On utilise le numéro et l'année pour l'unicité
                    _, created = Facture.objects.get_or_create(
                        num_facture=num_f,
                        annee_ex=str(row['Année']) if pd.notna(row['Année']) else "2025",
                        defaults={
                            # Attention : il y a un espace après 'Date ' dans ton Excel
                            'date_fact': row['Date '] if 'Date ' in df.columns and pd.notna(row['Date ']) else None,
                            'montant_facture': Decimal(str(row['Montant Facture'])) if pd.notna(row['Montant Facture']) else 0,
                            'validé': bool(row['Engagé']) if pd.notna(row['Engagé']) else False,
                            'payé': bool(row['Payé']) if pd.notna(row['Payé']) else False,
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Factures : {compteur} nouvelles ajoutées.")
        except Exception as e:
            print(f"❌ Erreur Factures : {e}")
def importer_ipm():
    chemin = r'table windev/Table IMP.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                valeur_ipm = row['IPM']
                if pd.notna(valeur_ipm):
                    # On utilise libelle_ipm car c'est le nom dans ton modèle
                    _, created = IPM.objects.get_or_create(
                        libelle_ipm=valeur_ipm,
                        defaults={'code_ipm': valeur_ipm} # On met la même chose dans code par défaut
                    )
                    if created: compteur += 1
            print(f"✅ IPM : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur IPM : {e}")

def importer_payements():
    chemin = r'table windev/Table Payement.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                # On utilise num_paiement et annee_ex selon ton modèle
                n_ordre = row['N° Ordre payment']
                if pd.notna(n_ordre):
                    _, created = Paiement.objects.get_or_create(
                        num_paiement=n_ordre,
                        # On ajoute l'année dans la recherche pour être précis
                        annee_ex=str(row['Année']) if pd.notna(row['Année']) else "2025",
                        defaults={
                            'date_payement': row['Date'] if pd.notna(row['Date']) else None,
                            'objet_payement': row['Objet'] if pd.notna(row['Objet']) else "",
                            'valider_pay': bool(row['valider']) if pd.notna(row['valider']) else False,
                        }
                    )
                    if created: compteur += 1
            print(f"✅ Paiements : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Paiements : {e}")
def importer_produits():
    chemin = r'table windev/Table Produit.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                _, created = Produit.objects.get_or_create(
                    compte=row['Compte'],
                    designation=row['Désignation'],
                    defaults={
                        'quantite': row['Quantité'] if pd.notna(row['Quantité']) else 0,
                        'unite': row['Unité'] if pd.notna(row['Unité']) else "",
                        'specification': row['Spécification'] if pd.notna(row['Spécification']) else "",
                        'observation': row['Observation'] if pd.notna(row['Observation']) else ""
                    }
                )
                if created: compteur += 1
            print(f"✅ Produits : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Produits : {e}")
    else:
        print(f"⚠️ Fichier introuvable : {chemin}")

def importer_membres():
    # Correction du nom : 'Membre commission' au lieu de 'NomMembreCommission'
    chemin = r'table windev/Table MembreCommision.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                # On utilise les noms exacts détectés dans ton fichier
                nom_membre = row['Membre commission']
                qualite_val = row['Qualité'] if pd.notna(row['Qualité']) else ""
                
                if pd.notna(nom_membre):
                    _, created = MembresCommission.objects.get_or_create(
                        nom_membre_commission=nom_membre,
                        defaults={'qualite': qualite_val}
                    )
                    if created: compteur += 1
            print(f"✅ Membres Commission : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Membres : {e}")
    else:
        print(f"⚠️ Fichier introuvable : {chemin}")

def importer_modes_reglement():
    # Correction du nom : 'Mode_pay' détecté dans ton fichier
    chemin = r'table windev/Table ModeDeReglement.xlsx'
    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            compteur = 0
            for _, row in df.iterrows():
                mode = row['Mode_pay']
                if pd.notna(mode):
                    _, created = ModeReglement.objects.get_or_create(
                        mode_pay=mode
                    )
                    if created: compteur += 1
            print(f"✅ Modes de Règlement : {compteur} nouveaux ajoutés.")
        except Exception as e:
            print(f"❌ Erreur Modes Règlement : {e}")
    else:
        print(f"⚠️ Fichier introuvable : {chemin}")

if __name__ == "__main__":
    print("--- DÉBUT DE L'IMPORTATION ---")
    importer_exercices()
    importer_comptes_principaux()
    importer_sous_comptes()
    importer_produits()
    importer_membres()
    importer_modes_reglement()
    importer_ipm()
    importer_payements()    
    importer_factures()
    importer_fournisseurs()
    importer_dbm()
    importer_depenses()
    importer_bons_engagement()
    importer_chapitres()
    importer_allocations()
    importer_technique()
    importer_types_budget()
    importer_utilisateurs()
    

    print("--- FIN DE L'IMPORTATION ---")