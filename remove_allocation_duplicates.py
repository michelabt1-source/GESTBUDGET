import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJETGCS.settings')
django.setup()

from django.db import transaction
from django.db.models import Count
from budget_app.models import AllocationBudget


def find_duplicates():
    return (
        AllocationBudget.objects
        .values('num_compte_principal', 'num_sous_compte', 'annee_ex')
        .annotate(count_id=Count('id'))
        .filter(count_id__gt=1)
        .order_by('num_compte_principal', 'num_sous_compte', 'annee_ex')
    )


def delete_duplicates():
    duplicates = find_duplicates()
    if not duplicates:
        print('Aucun doublon trouvé dans AllocationBudget.')
        return

    total_removed = 0
    with transaction.atomic():
        for dup in duplicates:
            queryset = AllocationBudget.objects.filter(
                num_compte_principal=dup['num_compte_principal'],
                num_sous_compte=dup['num_sous_compte'],
                annee_ex=dup['annee_ex'],
            ).order_by('id')

            keep = queryset.first()
            to_delete = queryset.exclude(pk=keep.pk)
            count = to_delete.count()
            if count:
                print(
                    f"Supprimer {count} doublon(s) pour compte principal={dup['num_compte_principal']} "
                    f"sous-compte={dup['num_sous_compte']} année={dup['annee_ex']} (garder id={keep.pk})"
                )
                to_delete.delete()
                total_removed += count

    print(f"Terminé : {total_removed} ligne(s) supprimée(s).")


if __name__ == '__main__':
    delete_duplicates()
