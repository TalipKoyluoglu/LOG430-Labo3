from magasin.models.magasin import Magasin
from magasin.models.stock import StockLocal
from magasin.models.vente import Vente
from magasin.models.ligneVente import LigneVente
from django.db.models import Sum, F  # type: ignore
from datetime import timedelta
from django.utils import timezone  # type: ignore


class UC3_PerformanceControleur:

    def get_indicateurs_par_magasin(self):
        resultats = []

        magasins = Magasin.objects.all()
        maintenant = timezone.now()
        semaine_dernier_jour = maintenant - timedelta(days=7)

        for magasin in magasins:
            
            chiffre_affaires = (
                LigneVente.objects.filter(vente__magasin=magasin)
                .annotate(total_ligne=F("quantite") * F("prix_unitaire"))
                .aggregate(total=Sum("total_ligne"))["total"]
                or 0
            )

            # Ruptures de stock
            ruptures = StockLocal.objects.filter(magasin=magasin, quantite=0).count()

            # Surstock
            surstock = StockLocal.objects.filter(
                magasin=magasin, quantite__gt=10
            ).count()

            # Tendances hebdo (basées sur les ventes des 7 derniers jours)
            ventes_recente = Vente.objects.filter(
                magasin=magasin, date_vente__gte=semaine_dernier_jour
            )
            lignes_recent = (
                LigneVente.objects.filter(vente__in=ventes_recente)
                .values("produit__nom")
                .annotate(total_vendu=Sum("quantite"))
                .order_by("-total_vendu")[:3]
            )

            tendances = [
                f"{ligne['produit__nom']} ({ligne['total_vendu']})"
                for ligne in lignes_recent
            ]

            resultats.append(
                {
                    "magasin": magasin.nom,
                    "chiffre_affaires": chiffre_affaires,
                    "ruptures": ruptures,
                    "surstock": surstock,
                    "tendances": ", ".join(tendances),
                }
            )

        return resultats
