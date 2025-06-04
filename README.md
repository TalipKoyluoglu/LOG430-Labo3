# LOG430 – Laboratoire 1 : Architecture 2 tiers - (Client/Serveur), Persistance avec PostgreSQL

## Description de l'application

Ce projet constitue le développement d’un système de caisse simulant un petit magasin avec trois caisses pouvant fonctionner en simultané. Il applique une architecture client/serveur (2 tiers) : une application console en Python agissant comme client, et une base de données PostgreSQL servant de serveur de persistance. Le tout est orchestré avec Docker et Docker Compose, testé automatiquement avec `pytest`, et déployé via une pipeline CI/CD GitHub Actions.

Ce laboratoire comprend également la production de documents techniques selon le modèle 4+1 (vue logique, vue d’implémentation, vue de déploiement, cas d’utilisation), ainsi que la documentation des choix sous forme d'ADR (Architectural Decision Records).

---

## Structure du projet

```plaintext
.
├── .github/workflows/
│   └── ci.yml                     # Pipeline CI/CD GitHub Actions
├── src/
│   ├── db/
│   │   ├── models.py              # Modèles ORM SQLAlchemy
│   │   └── session.py             # Configuration de la base PostgreSQL
│   ├── logic/
│   │   └── caisse.py              # Logique métier (ajout, vente, annulation...)
│   └── main.py                    # Menu console (interface utilisateur)
├── tests/
│   ├── conftest.py                # Base temporaire pour tests
│   └── test_caisse.py             # Tests unitaires Pytest
├── docs/
│   ├── ADR/
│   │   └── ADR-003-strategie-persistance.md   # Stratégie de persistance SQLAlchemy + PostgreSQL
│   │   └── ADR-004-bdd-postgresql.md          # Justification du choix de PostgreSQL
│   └── UML/
│       └── DSS-afficherStock.puml             # Diagramme de séquence : afficher le stock
│       └── DSS-ajouterProduit.puml            # Diagramme de séquence : ajouter un produit
│       └── DSS-annulerVente.puml              # Diagramme de séquence : annuler une vente
│       └── DSS-enregistrerVente.puml          # Diagramme de séquence : enregistrer une vente
│       └── DSS-rechercherProduit.puml         # Diagramme de séquence : rechercher un produit
│       └── vue-cas-utilisation.puml           # Vue des cas d'utilisation
│       └── vue-deploiement.puml               # Vue de déploiement (2-tier)
│       └── vue-implementation.puml            # Vue d'implémentation (structure modules)
│       └── vue-logique.puml                   # Vue logique
├── Dockerfile                   # Construction de l’image Docker
├── docker-compose.yml           # Orchestration des services (app + PostgreSQL)
├── requirements.txt             # Dépendances Python (sqlalchemy, psycopg2, pytest)
├── pytest.ini                   # Configuration du chemin d'import Python
└── README.md                    # Documentation principale du projet
```

---

## Cloner et démarrer le projet

```bash
git clone https://github.com/TalipKoyluoglu/LOG430-Lab1.git
cd LOG430-Lab1
```

---

## Fonctionnalités principales

- Rechercher un produit
- Ajouter / Approvisionner un produit
- Afficher le stock
- Enregistrer une vente
- Annuler une vente (stock restauré)
- Gestion transactionnelle via SQLAlchemy ORM
- Persistance avec PostgreSQL
- Affichage des ventes, gestion multi-produits, affichage tabulaire

---

## Conteneurisation avec Docker & PostgreSQL

Le système repose sur deux services :

1. **postgres** : base de données PostgreSQL 15  
2. **caisse-app** : application console Python (interactive avec `input()`)

Volume persistant `pgdata` utilisé pour conserver la base entre les redémarrages.

---

## Lancer 3 caisses simultanément avec Docker Compose

Cette section vous permet de simuler l'utilisation de **trois caisses différentes** en même temps, chacune dans son propre terminal.

---

### Étape 1 – Démarrer l’infrastructure (base de données)

Dans un **premier terminal**, lancez :

```bash
docker-compose up
```

Ce terminal garde la base de données PostgreSQL active. **Laissez-le ouvert**.

---

### Étape 2 – Ouvrir 3 caisses dans 3 terminaux séparés

Ouvrez **3 nouveaux terminaux** (ou onglets) et exécutez cette commande dans **chacun d’eux** :

```bash
docker-compose run --rm caisse-app
```

Chaque instance de cette commande ouvre une **session de caisse indépendante** connectée à la **même base de données**.

Vous aurez ainsi :

- Une première caisse dans le terminal 2
- Une deuxième caisse dans le terminal 3
- Une troisième caisse dans le terminal 4

---

### Exemple d’organisation des terminaux

```plaintext
Terminal 1 : docker-compose up                   (postgres actif)
Terminal 2 : docker-compose run --rm caisse-app  (caisse #1)
Terminal 3 : docker-compose run --rm caisse-app  (caisse #2)
Terminal 4 : docker-compose run --rm caisse-app  (caisse #3)
```

---

### 🧼 Étape 3 – Fermer proprement

Quand vous avez terminé :

1. Fermez les 3 terminaux de caisse (ou faites `Ctrl+C`)
2. Dans le terminal 1, appuyez sur `Ctrl+C` pour stopper `docker-compose up`
3. Puis exécutez :

```bash
docker-compose down
```

Cela arrête et supprime tous les conteneurs liés au projet.


## Utilisation directe (PowerShell) sans le code source

### 1. Lancer la base PostgreSQL :

```powershell
docker run -d --name log430-postgres `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=caisse `
  -p 55432:5432 `
  postgres:15
```

### 2. Lancer l’application :

```powershell
docker run --rm -it `
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:55432/caisse `
  talipkoyluoglu/log430-lab1:latest
```

### 3. Ouvrir 3 caisses :

Répétez la commande ci-dessus dans 3 terminaux différents pour simuler 3 caisses.

### 4. Nettoyer :

```powershell
docker stop log430-postgres
docker rm log430-postgres
```

---

## Fonctionnement de la pipeline CI/CD (GitHub Actions)

Le pipeline CI/CD se déclenche à chaque `push` ou `pull request` sur la branche `lab1-main`.

### Étapes de la pipeline :

1. Checkout du dépôt  
2. Installation de Python 3.11  
3. Installation de `black`, `pytest`, `sqlalchemy`, `psycopg2`  
4. Vérification du style avec `black`  
5. Exécution des tests unitaires (`pytest`)  
6. Build Docker de l’application  
7. Connexion sécurisée à Docker Hub (via `DOCKER_USERNAME` et `DOCKER_PASSWORD`)  
8. Push automatique de l’image :  
   `docker.io/talipkoyluoglu/log430-lab1:latest`

---

## Choix techniques

| Élément              | Justification                                                                 |
|----------------------|------------------------------------------------------------------------------|
| **Python 3.11**      | Langage simple et maintenu, idéal pour les scripts console                    |
| **SQLAlchemy ORM**   | Abstraction des accès base, code modulaire et portable                        |
| **PostgreSQL**       | Meilleure gestion du multi-utilisateur que SQLite                             |
| **Docker**           | Environnement reproductible et déployable                                     |
| **Docker Compose**   | Orchestration multi-services : caisse-app + base de données                   |
| **GitHub Actions**   | Intégration continue automatisée, push image vers Docker Hub                  |
| **Black**            | Formatage uniforme et rigoureux du code source                                |
| **Pytest**           | Tests unitaires rapides et efficaces                                          |
| **Modèle 4+1**       | Documentation de l’architecture : cas d’utilisation, logique, déploiement...  |
| **ADR**              | Justification explicite des choix architecturaux                              |

---

## Exécution de la pipeline CI/CD

✅ Voir la pipeline CI/CD sur GitHub :  
https://github.com/TalipKoyluoglu/LOG430-Lab1/actions/runs/15217477282

---

## Auteur

Projet réalisé par Talip Koyluoglu dans le cadre du cours LOG430 à l'ÉTS.

---

## Ressources utiles

- Docker : https://docs.docker.com/get-started/  
- GitHub Actions : https://docs.github.com/en/actions  
- SQLAlchemy : https://docs.sqlalchemy.org/  
- Pytest : https://docs.pytest.org/  
- Black : https://black.readthedocs.io/en/stable/
