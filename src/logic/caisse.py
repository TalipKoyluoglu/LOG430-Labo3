from db.models import Produit, Vente, LigneVente
from datetime import datetime, timezone


def ajouter_produit(session):
    nom = input("Nom du produit : ")
    categorie = input("Catégorie : ")
    prix = float(input("Prix : "))
    quantite = int(input("Quantité à ajouter : "))

    produit = session.query(Produit).filter_by(nom=nom).first()
    if produit:
        print("[INFO] Produit déjà existant, on augmente le stock.")
        produit.quantiteStock += quantite
    else:
        print("[INFO] Produit inexistant, on l'ajoute.")
        produit = Produit(
            nom=nom, categorie=categorie, prix=prix, quantiteStock=quantite
        )
        session.add(produit)

    session.commit()
    print("[INFO] Produit ajouté ou mis à jour avec succès.")


def rechercher_produit(session):
    nom = input("Nom du produit à rechercher : ")
    produits = session.query(Produit).filter(Produit.nom.ilike(f"%{nom}%")).all()

    if not produits:
        print("[INFO] Aucun produit trouvé.")
        return

    print("\n--- RÉSULTATS DE RECHERCHE ---")
    print(f"{'ID':<5} {'Nom':<20} {'Catégorie':<15} {'Stock':<8} {'Prix ($)':<8}")
    print("-" * 60)

    for p in produits:
        print(
            f"{p.id:<5} {p.nom:<20} {p.categorie:<15} {p.quantiteStock:<8} {p.prix:<8.2f}"
        )

    print("-" * 60)


def afficher_stock(session):
    produits = session.query(Produit).all()

    if not produits:
        print("[INFO] Aucun produit en stock.")
        return

    print("\n--- STOCK ACTUEL ---")
    print(f"{'ID':<5} {'Nom':<20} {'Catégorie':<15} {'Stock':<8} {'Prix ($)':<8}")
    print("-" * 60)

    for p in produits:
        print(
            f"{p.id:<5} {p.nom:<20} {p.categorie:<15} {p.quantiteStock:<8} {p.prix:<8.2f}"
        )

    print("-" * 60)


def enregistrer_vente(session):
    afficher_stock(session)
    ids = input("Entrez les IDs des produits à acheter (séparés par des virgules) : ")
    ids = [int(i.strip()) for i in ids.split(",")]

    lignes_vente = []
    total = 0

    for pid in ids:
        produit = session.query(Produit).filter_by(id=pid).first()
        if not produit:
            print(f"[ERREUR] Produit ID {pid} introuvable.")
            continue

        print(f"Produit : {produit.nom} - Stock : {produit.quantiteStock}")
        quantite = int(input(f"Quantité désirée pour {produit.nom} : "))
        if quantite > produit.quantiteStock:
            print(f"[ERREUR] Stock insuffisant pour {produit.nom}.")
            continue

        produit.quantiteStock -= quantite
        sous_total = quantite * produit.prix
        total += sous_total

        ligne = LigneVente(produit_id=pid, quantite=quantite, sousTotal=sous_total)
        lignes_vente.append(ligne)

    vente = Vente(date=datetime.now(timezone.utc), total=total, lignes=lignes_vente)
    session.add(vente)
    session.commit()
    print(f"[INFO] Vente enregistrée. Total : {total:.2f} $")


def annuler_vente(session):
    ventes = session.query(Vente).all()

    if not ventes:
        print("[INFO] Aucune vente à annuler.")
        return

    print("\n--- VENTES ENREGISTRÉES ---")
    print(f"{'ID':<5} {'Produit':<20} {'Qté':<5} {'Date':<20} {'Total ($)':<10}")
    print("-" * 70)

    for v in ventes:
        for ligne in v.lignes:
            produit = session.query(Produit).filter_by(id=ligne.produit_id).first()
            nom_produit = produit.nom if produit else "Inconnu"
            date_str = v.date.strftime("%Y-%m-%d %H:%M")
            print(
                f"{v.id:<5} {nom_produit:<20} {ligne.quantite:<5} {date_str:<20} {v.total:<10.2f}"
            )

    print("-" * 70)

    try:
        vente_id = int(input("ID de la vente à annuler : "))
    except ValueError:
        print("[ERREUR] Entrée invalide.")
        return

    vente = session.query(Vente).filter_by(id=vente_id).first()
    if not vente:
        print("[ERREUR] Vente introuvable.")
        return

    # Rétablir le stock
    for ligne in vente.lignes:
        produit = session.query(Produit).filter_by(id=ligne.produit_id).first()
        if produit:
            produit.quantiteStock += ligne.quantite

    session.delete(vente)
    session.commit()
    print(f"[INFO] Vente {vente_id} annulée avec succès.")
