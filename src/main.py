from db.session import init_db, SessionLocal
from logic.caisse import (
    ajouter_produit,
    rechercher_produit,
    afficher_stock,
    enregistrer_vente,
    annuler_vente,
)


def main():
    print("[INFO] Initialisation de la base de données...")
    init_db()
    print("[INFO] Base initialisée.")

    session = SessionLocal()

    while True:
        print("\n=== MENU CAISSE ===")
        print("1. Rechercher un produit")
        print("2. Ajouter / Approvisionner un produit")
        print("3. Afficher tout le stock")
        print("4. Enregistrer une vente")
        print("5. Annuler une vente")
        print("0. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            rechercher_produit(session)
        elif choix == "2":
            ajouter_produit(session)
        elif choix == "3":
            afficher_stock(session)
        elif choix == "4":
            enregistrer_vente(session)
        elif choix == "5":
            annuler_vente(session)
        elif choix == "0":
            print("Fermeture de la caisse...")
            break
        else:
            print("Choix invalide.")

    session.close()


if __name__ == "__main__":
    main()
