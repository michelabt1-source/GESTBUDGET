import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJETGCS.settings')
django.setup()

from budget_app.models import NumComptePrincipal, SousCompte


def link_sous_comptes_to_comptes_principaux():
    """
    Automatise la liaison entre les sous-comptes et leurs comptes principaux
    basé sur les premiers chiffres du numéro de sous-compte.
    """
    updates = 0
    skipped = 0

    # Récupérer tous les sous-comptes sans compte principal
    sous_comptes_orphans = SousCompte.objects.filter(compte_principal__isnull=True)

    for sous_compte in sous_comptes_orphans:
        compte_principal_trouve = None

        # Essayer de trouver le compte principal en se basant sur les premiers chiffres
        num_sous_compte = str(sous_compte.num_sous_compte).replace('.0', '')  # Enlever .0 à la fin

        # Tester différents longueurs de préfixe (du plus spécifique au plus général)
        for prefix_length in [4, 3, 2]:  # Essayer d'abord 4 chiffres, puis 3, puis 2
            if len(num_sous_compte) >= prefix_length:
                prefix = num_sous_compte[:prefix_length]
                try:
                    compte_principal = NumComptePrincipal.objects.get(num_compte_principal=prefix)
                    compte_principal_trouve = compte_principal
                    break
                except NumComptePrincipal.DoesNotExist:
                    continue

        if compte_principal_trouve:
            sous_compte.compte_principal = compte_principal_trouve
            sous_compte.save(update_fields=['compte_principal'])
            updates += 1
            print(f"✅ Lié {sous_compte.num_sous_compte} à {compte_principal_trouve.num_compte_principal}")
        else:
            print(f"❌ Aucun compte principal trouvé pour {sous_compte.num_sous_compte}")
            skipped += 1

    print(f"\nRésultat : {updates} sous-comptes liés, {skipped} non trouvés.")


if __name__ == '__main__':
    link_sous_comptes_to_comptes_principaux()