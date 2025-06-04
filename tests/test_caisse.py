from db.models import Produit, Vente
from logic import caisse


def test_ajouter_nouveau_produit(session, monkeypatch):
    inputs = iter(["Stylo", "Fourniture", "2.50", "100"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    caisse.ajouter_produit(session)
    produit = session.query(Produit).filter_by(nom="Stylo").first()
    assert produit is not None
    assert produit.quantiteStock == 100
    assert produit.prix == 2.50


def test_augmenter_stock_produit_existant(session, monkeypatch):
    # Préparer produit existant
    produit = Produit(nom="Stylo", categorie="Fourniture", prix=2.50, quantiteStock=50)
    session.add(produit)
    session.commit()

    # Ajout via input
    inputs = iter(["Stylo", "Fourniture", "2.50", "30"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    caisse.ajouter_produit(session)

    produit = session.query(Produit).filter_by(nom="Stylo").first()
    assert produit.quantiteStock == 80


def test_rechercher_produit_affiche_resultat(session, capsys, monkeypatch):
    produit = Produit(nom="Cahier", categorie="Papeterie", prix=1.99, quantiteStock=30)
    session.add(produit)
    session.commit()

    monkeypatch.setattr("builtins.input", lambda _: "Cahier")
    caisse.rechercher_produit(session)

    captured = capsys.readouterr()
    assert "Cahier" in captured.out
    assert "Papeterie" in captured.out


def test_enregistrer_vente_met_a_jour_stock(session, monkeypatch):
    produit = Produit(nom="Livre", categorie="Culture", prix=10.0, quantiteStock=10)
    session.add(produit)
    session.commit()

    inputs = iter(["1", "2"])  # ID du produit, puis quantité
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    caisse.enregistrer_vente(session)

    produit = session.query(Produit).filter_by(id=1).first()
    assert produit.quantiteStock == 8

    vente = session.query(Vente).first()
    assert vente.total == 20.0


def test_annuler_vente_retablit_stock(session, monkeypatch):
    produit = Produit(nom="Gomme", categorie="Fourniture", prix=0.50, quantiteStock=5)
    session.add(produit)
    session.commit()

    # Créer vente manuellement
    from db.models import Vente, LigneVente

    ligne = LigneVente(produit=produit, quantite=2, sousTotal=1.0)
    vente = Vente(total=1.0, lignes=[ligne])
    session.add(vente)
    produit.quantiteStock -= 2
    session.commit()

    monkeypatch.setattr("builtins.input", lambda _: "1")
    caisse.annuler_vente(session)

    produit = session.query(Produit).filter_by(nom="Gomme").first()
    assert produit.quantiteStock == 5
    assert session.query(Vente).count() == 0


def test_cycle_ajout_vente_annulation(session, monkeypatch):
    # Étape 1 : ajout du produit
    inputs_ajout = iter(["Crayon", "Fourniture", "1.00", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_ajout))
    caisse.ajouter_produit(session)

    produit = session.query(Produit).filter_by(nom="Crayon").first()
    assert produit is not None
    assert produit.quantiteStock == 10

    # Étape 2 : enregistrement d'une vente (ID 1, quantité 3)
    inputs_vente = iter(["1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs_vente))
    caisse.enregistrer_vente(session)

    produit = session.query(Produit).filter_by(id=1).first()
    assert produit.quantiteStock == 7  # 10 - 3

    vente = session.query(Vente).first()
    assert vente.total == 3.00
    assert len(vente.lignes) == 1

    # Étape 3 : annulation de la vente
    monkeypatch.setattr("builtins.input", lambda _: "1")
    caisse.annuler_vente(session)

    produit = session.query(Produit).filter_by(id=1).first()
    assert produit.quantiteStock == 10  # stock restauré
    assert session.query(Vente).count() == 0
