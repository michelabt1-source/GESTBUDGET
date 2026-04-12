import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJETGCS.settings')
django.setup()

from budget_app.models import AllocationBudget, SousCompte


def fill_sous_compte_relations():
    updates = 0
    skipped = 0
    ambiguous = 0

    allocations = AllocationBudget.objects.filter(sous_compte__isnull=True)
    for alloc in allocations:
        candidate = None

        # 1) d'abord, essayer de retrouver par le numéro de sous-compte existant
        if alloc.num_sous_compte:
            candidate = SousCompte.objects.filter(num_sous_compte=alloc.num_sous_compte).first()

        # 2) si on n'a pas trouvé par le numéro, on tente par le libellé du sous-compte
        if not candidate and alloc.libelle_sous_compte:
            possibles = SousCompte.objects.filter(libelle_sous_compte=alloc.libelle_sous_compte)
            if possibles.count() == 1:
                candidate = possibles.first()
            elif possibles.count() > 1:
                print(f"⚠️ Multiple match pour AllocationBudget id={alloc.id}: libelle='{alloc.libelle_sous_compte}'")
                ambiguous += 1
                continue

        if candidate:
            alloc.sous_compte = candidate
            if not alloc.num_sous_compte:
                alloc.num_sous_compte = candidate.num_sous_compte
            if not alloc.libelle_sous_compte:
                alloc.libelle_sous_compte = candidate.libelle_sous_compte
            alloc.save(update_fields=['sous_compte', 'num_sous_compte', 'libelle_sous_compte'])
            updates += 1
        else:
            print(f"❌ Aucun SousCompte trouvé pour AllocationBudget id={alloc.id}: num_sous_compte='{alloc.num_sous_compte}' libelle='{alloc.libelle_sous_compte}'")
            skipped += 1

    print(f"\nRésultat : {updates} allocations mises à jour, {skipped} non trouvées, {ambiguous} ambiguïtés.")


if __name__ == '__main__':
    fill_sous_compte_relations()
