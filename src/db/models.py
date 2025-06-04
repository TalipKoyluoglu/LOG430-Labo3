from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    categorie = Column(String, nullable=False)
    prix = Column(Float, nullable=False)
    quantiteStock = Column(Integer, nullable=False)


class Vente(Base):
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now(timezone.utc))
    total = Column(Float, nullable=False)

    lignes = relationship("LigneVente", back_populates="vente", cascade="all, delete")


class LigneVente(Base):
    __tablename__ = "lignes_vente"

    id = Column(Integer, primary_key=True)
    vente_id = Column(Integer, ForeignKey("ventes.id"))
    produit_id = Column(Integer, ForeignKey("produits.id"))
    quantite = Column(Integer, nullable=False)
    sousTotal = Column(Float, nullable=False)

    vente = relationship("Vente", back_populates="lignes")
    produit = relationship("Produit")
