from django.core.management.base import BaseCommand
from budget_app.models import AllocationBudget, NumComptePrincipal, SousCompte

class Command(BaseCommand):
    help = 'Relie les allocations aux sous-comptes existants'

    def handle(self, *args, **kwargs):
        allocations = AllocationBudget.objects.filter(sous_compte__isnull=True)
        for alloc in allocations:
            candidate = None

            if alloc.num_sous_compte:
                candidate = SousCompte.objects.filter(num_sous_compte=alloc.num_sous_compte).first()

            if not candidate and alloc.libelle_sous_compte:
                possibles = SousCompte.objects.filter(libelle_sous_compte=alloc.libelle_sous_compte)
                if possibles.count() == 1:
                    candidate = possibles.first()
                elif possibles.count() > 1:
                    self.stdout.write(self.style.WARNING(
                        f"Plusieurs correspondances pour AllocationBudget id={alloc.id}: libelle_sous_compte='{alloc.libelle_sous_compte}'"
                    ))
                    continue

            if candidate:
                alloc.sous_compte = candidate
                alloc.save(update_fields=['sous_compte'])
                self.stdout.write(self.style.SUCCESS(f"Lié : AllocationBudget id={alloc.id} -> SousCompte {candidate}"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Aucun sous-compte trouvé pour AllocationBudget id={alloc.id}: num_sous_compte='{alloc.num_sous_compte}'"
                ))
def lier_structure_comptable():
    sous_comptes = SousCompte.objects.all()
    liens_crees = 0
    erreurs = 0

    for sc in sous_comptes:
        # On essaie de déterminer le numéro du parent
        # Si sc.num_sous_compte est "20.01.01", le parent est "20"
        if "." in sc.num_sous_compte:
            prefixe_parent = sc.num_sous_compte.split('.')[0]
        else:
            # Si pas de point, on ne peut pas deviner, on passe
            continue

        try:
            # On cherche l'objet parent correspondant
            parent_obj = NumComptePrincipal.objects.get(num_compte_principal=prefixe_parent)
            
            # On fait la liaison
            sc.compte_principal = parent_obj
            sc.save(update_fields=['compte_principal'])
            liens_crees += 1
            print(f"✅ Lié : {sc.num_sous_compte} -> Parent {prefixe_parent}")
            
        except NumComptePrincipal.DoesNotExist:
            erreurs += 1
            print(f"⚠️ Parent introuvable pour : {sc.num_sous_compte} (cherché: {prefixe_parent})")

    print(f"\n--- RAPPORT ---")
    print(f"Liaisons réussies : {liens_crees}")
    print(f"Parents manquants : {erreurs}")

# Lancer la fonction
lier_structure_comptable()