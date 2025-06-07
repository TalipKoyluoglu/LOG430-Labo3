from magasin.models.stock import DemandeReapprovisionnement, StockCentral, StockLocal


class UC6_ValidationControleur:

    def get_demandes_en_attente(self):
        return DemandeReapprovisionnement.objects.filter(statut="en_attente")

    def valider_demande(self, demande_id):
        try:
            demande = DemandeReapprovisionnement.objects.get(id=demande_id)
            print(
                f" Demande trouvée : {demande.produit.nom} {demande.quantite} pour {demande.magasin.nom}"
            )

            produit = demande.produit
            magasin = demande.magasin
            quantite = demande.quantite

            stock_central = StockCentral.objects.get(produit=produit)
            print(f" StockCentral initial : {stock_central.quantite}")

            if quantite <= 0 or stock_central.quantite < quantite:
                print(" Quantité insuffisante dans le stock central")
                demande.statut = "refusée"
                demande.save()
                return False

            stock_local, created = StockLocal.objects.get_or_create(
                produit=produit, magasin=magasin, defaults={"quantite": 0}
            )
            print(
                f" StockLocal {'créé' if created else 'existant'} avec {stock_local.quantite} unités"
            )

            stock_central.quantite -= quantite
            stock_local.quantite += quantite

            stock_central.save()
            stock_local.save()

            demande.statut = "approuvée"
            demande.save()

            print(" Transfert terminé")
            return True

        except DemandeReapprovisionnement.DoesNotExist:
            return False
        except Exception as e:
            print(f"[ERREUR] UC6 - Validation échouée : {e}")
            return False

    # Maintenant correctement indentée dans la classe
    def rejeter_demande(self, demande_id):
        try:
            demande = DemandeReapprovisionnement.objects.get(id=demande_id)
            demande.statut = "refusée"
            demande.save()
            print(f" Demande {demande_id} rejetée manuellement.")
            return True
        except DemandeReapprovisionnement.DoesNotExist:
            print(f"[ERREUR] Demande {demande_id} introuvable.")
            return False
        except Exception as e:
            print(f"[ERREUR] UC6 - Rejet échoué : {e}")
            return False
