# LOG430 – Laboratoire 2 : Architecture 3 tiers, Django MVC - Multi-Magasins avec PostgreSQL

## Description de l'application

Ce projet est une extension du laboratoire 1, basé sur le framework Django. Il simule un système multi-magasins permettant la gestion du stock central, la répartition des produits, les ventes locales et la validation des demandes de réapprovisionnement.

Le laboratoire 2 introduit une architecture web de type **MVC** avec Django, une base de données PostgreSQL conteneurisée, ainsi qu’un pipeline CI/CD complet incluant les tests (unitaires, intégration, e2e) et le déploiement d’un conteneur Docker.

---

## Structure du projet

```plaintext
.
├── magasin/
│   ├── models/                        # Modèles ORM Django
│   ├── views/                         # Logique applicative (views/controllers)
│   ├── templates/                     # Fichiers HTML
│   │── controllers/                   # logique métier 
│   ├── tests/
│   │   ├── test_unitaires.py         # Tests unitaires
│   │   ├── test_integration.py       # Tests d'intégration
│   │   ├── test_e2e.py               # Tests end-to-end
│   │   └── conftest.py               # Configuration des tests
│   └── urls.py                       # Routes de l'application
├── config/
│   └── settings.py                   # Paramètres Django (connexion PostgreSQL)
├── docs/
│   ├── ADR/
│   │   ├── ADR-001.md                # Adoption de la structure MVC (Model-View-Controller) avec Django
│   │   ├── ADR-002.md                # Adoption de l’ORM intégré de Django pour la gestion de la persistance
│   │  
│   └── UML/
│       ├── DSS-creer-demande-approvisionnement.puml    # Diagramme de séquence : création de la demande d'approvisionnement
│       ├── DSS-modifierProduit.puml                    # Diagramme de séquence : modification du produit
│       ├── DSS-valider-demande-approvisionnement.puml  # Diagramme de séquence : validation de la demande d'approvisionnement
│       ├── vue-logique.puml          # Vue logique
│       ├── vue-deploiement.puml      # Vue de déploiement
│       ├── vue-implementation.puml   # Vue d'implémentation
│       └── vue-cas-utilisation.puml  # Vue des cas d'utilisation
│   └── arc42.md                      # Rapport sous la forme de template arc42
├── Dockerfile                        # Construction de l’image Docker
├── docker-compose.yml                # Orchestration des services (app + PostgreSQL)
├── requirements.txt                  # Installation des dépendances
├── pytest.ini 
└── README.md                         # Documentation principale du projet
```

---

## Démarrage rapide

```bash
git clone https://github.com/TalipKoyluoglu/LOG430-Labo2.git
cd LOG430-Labo2
docker-compose up --build
```

---

## Fonctionnalités principales

- Gestion des produits et du stock central
- Visualisation du stock local par magasin
- Création de demandes de réapprovisionnement
- Validation de demande de réapprovisionnement via la maison-mère
- Génération de rapports de performance
- Création et visualisation des ventes locales
- Interface web minimaliste avec templates HTML

---

## Tests automatisés

Les tests sont organisés en 3 catégories :

-  **Tests unitaires** (`test_unitaires.py`)
-  **Tests d’intégration** (`test_integration.py`)
-  **Tests end-to-end** (`test_e2e.py`)

Exécution des tests :

```bash
docker-compose run web pytest magasin/tests/
```

---

## Pipeline CI/CD

Déclenchée à chaque `push` ou `pull request` sur `main`.

### Étapes :

1. Vérification du style (`black`)
2. Lancement de PostgreSQL + Django en conteneur
3. Exécution des tests Pytest (unitaires, intégration, e2e)
4. Build de l’image Docker
5. Déploiement automatique sur Docker Hub (`docker.io/talipkoyluoglu/log430-labo2:latest`)

---

Voir la pipeline GitHub :  

Pipeline réussie : https://github.com/TalipKoyluoglu/LOG430-Labo2/actions/runs/15550082635

---

## Architecture (Modèle 4+1)

Ce projet inclut une documentation complète de l’architecture :

-  Vue logique (`vue-logique.puml`)
-  Vue d’implémentation (`vue-implementation.puml`)
-  Vue de déploiement (`vue-deploiement.puml`)
-  Cas d’utilisation (`vue-cas-utilisation.puml`)
-  DSS (diagrammes de séquence système) pour 3 cas clés

---
## Cas d'utilisation traités

- Ajouter un produit
- Créer une demande de réapprovisionnement
- Valider une demande
- Gérer le stock central et local
- Générer un rapport de performance

---   

## Choix techniques

| Élément              | Justification                                                                 |
|----------------------|------------------------------------------------------------------------------|
| **Django MVC**       | Architecture web robuste, séparation claire des responsabilités               |
| **PostgreSQL**       | Base de données relationnelle performante et compatible ORM Django            |
| **Docker Compose**   | Orchestration des conteneurs (web + base de données)                          |
| **Pytest**           | Framework de tests modulaire et structuré                                     |
| **GitHub Actions**   | Automatisation CI/CD (tests, build, déploiement)                              |
| **Black**            | Conventions de style automatiques pour un code propre                         |
| **ADR**              | Documentation formelle des décisions d’architecture                           |
| **PlantUML**         | Génération automatisée des diagrammes d’architecture                          |

---

## Auteur

Projet réalisé par Talip Koyluoglu. 

