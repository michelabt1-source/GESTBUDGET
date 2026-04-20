import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJETGCS.settings')
django.setup()

from budget_app.models import SousCompte


def automatiser_liaisons_plan_comptable():
    """
    Script principal pour automatiser les liaisons dans le plan comptable.
    Met à jour tous les sous-comptes orphelins pour les lier à leur compte principal.
    """
    print("🚀 Automatisation des liaisons Plan Comptable")
    print("=" * 50)

    # Compter les sous-comptes orphelins avant
    orphelins_avant = SousCompte.objects.filter(compte_principal__isnull=True).count()
    print(f"Sous-comptes sans compte principal avant: {orphelins_avant}")

    updates = 0
    skipped = 0

    # Traiter tous les sous-comptes orphelins
    sous_comptes_orphans = SousCompte.objects.filter(compte_principal__isnull=True)

    for sous_compte in sous_comptes_orphans:
        # La méthode save() va automatiquement lier le compte principal
        # On force une sauvegarde pour déclencher la logique automatique
        old_compte_principal = sous_compte.compte_principal
        sous_compte.save()  # Cela déclenche la méthode _find_compte_principal()

        if sous_compte.compte_principal != old_compte_principal:
            updates += 1
            print(f"✅ Lié {sous_compte.num_sous_compte} → {sous_compte.compte_principal}")
        else:
            skipped += 1
            print(f"❌ Non lié: {sous_compte.num_sous_compte}")

    # Résumé final
    orphelins_apres = SousCompte.objects.filter(compte_principal__isnull=True).count()
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS FINAUX:")
    print(f"• Sous-comptes liés: {updates}")
    print(f"• Sous-comptes non trouvés: {skipped}")
    print(f"• Orphelins restants: {orphelins_apres}")
    print(f"• Total sous-comptes: {SousCompte.objects.count()}")

    if updates > 0:
        print("\n✅ Automatisation réussie! Les liaisons sont maintenant automatiques.")
    else:
        print("\nℹ️ Tous les sous-comptes sont déjà liés ou aucun n'a pu être automatisé.")


if __name__ == '__main__':
    automatiser_liaisons_plan_comptable()