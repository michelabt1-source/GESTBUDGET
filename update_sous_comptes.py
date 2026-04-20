import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJETGCS.settings')
django.setup()

from budget_app.models import SousCompte


def update_existing_sous_comptes():
    """
    Met à jour tous les sous-comptes existants pour lier automatiquement
    leur compte principal si ce n'est pas déjà fait.
    """
    updates = 0
    skipped = 0

    # Récupérer tous les sous-comptes sans compte principal
    sous_comptes_orphans = SousCompte.objects.filter(compte_principal__isnull=True)

    for sous_compte in sous_comptes_orphans:
        # Utiliser la méthode _find_compte_principal du modèle
        compte_principal = sous_compte._find_compte_principal()

        if compte_principal:
            sous_compte.compte_principal = compte_principal
            sous_compte.save(update_fields=['compte_principal'])
            updates += 1
            print(f"✅ Lié {sous_compte.num_sous_compte} à {compte_principal.num_compte_principal}")
        else:
            print(f"❌ Aucun compte principal trouvé pour {sous_compte.num_sous_compte}")
            skipped += 1

    print(f"\nRésultat : {updates} sous-comptes mis à jour, {skipped} non trouvés.")


if __name__ == '__main__':
    update_existing_sous_comptes()