# LOG430 – Laboratoire 3 : API REST pour un système multi-magasins

## Description de l'application

Ce projet implémente un système de gestion multi-magasins avec une **API REST complète** développée avec Django et Django REST Framework. Le système permet la gestion des produits, des stocks, des ventes et des demandes de réapprovisionnement à travers deux interfaces :

- **Interface Web traditionnelle** : Vues Django avec templates HTML
- **API REST** : Points d'accès JSON documentés avec Swagger/OpenAPI

L'architecture respecte une séparation claire des responsabilités avec une couche de services dédiée à la logique métier, permettant aux contrôleurs web et API d'accéder aux mêmes fonctionnalités sans duplication de code.

---

## Structure du projet

```plaintext
LOG430-Labo3/
├── config/                           # Configuration Django
│   ├── settings.py                   # Paramètres (DB, API, CORS)
│   ├── urls.py                       # URLs racine
│   └── wsgi.py                       # Configuration WSGI
├── magasin/                          # Application principale
│   ├── api/                          # Couche API REST
│   │   ├── controllers/              # Contrôleurs API (UC1-UC4)
│   │   ├── serializers/              # Sérialiseurs JSON
│   │   ├── tests/                    # Tests d'API
│   │   ├── auth.py                   # Authentification par token
│   │   ├── urls.py                   # Routes API (/api/v1/...)
│   │   └── swagger_urls.py           # Documentation Swagger
│   ├── services/                     # Couche logique métier
│   │   ├── uc1_service.py            # Service rapport ventes
│   │   ├── uc2_service.py            # Service gestion stock
│   │   ├── uc3_service.py            # Service performances
│   │   ├── uc4_service.py            # Service gestion produits
│   │   └── uc6_service.py            # Service validation demandes
│   ├── controllers/                  # Logique pour vues web
│   ├── views/                        # Vues Django (présentation web)
│   ├── models/                       # Modèles de données (ORM)
│   ├── templates/                    # Templates HTML
│   └── tests/                        # Tests (unitaires, intégration, e2e)
├── docs/                             # Documentation
│   ├── UML/                          # Diagrammes d'architecture
│   └── ADR/                          # Décisions d'architecture
├── docker-compose.yml                # Orchestration des services
├── Dockerfile                        # Image de l'application
├── requirements.txt                  # Dépendances Python
├── pytest.ini                       # Configuration des tests
└── README.md                         # Cette documentation
```

---

## Démarrage rapide

### Prérequis
- Docker et Docker Compose installés
- Port 8000 et 5432 disponibles (ou modifier dans docker-compose.yml)

### Lancement de l'application

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/TalipKoyluoglu/LOG430-Labo3.git
   cd LOG430-Labo3
   ```

2. **Démarrer avec Docker Compose** :
   ```bash
   docker-compose up --build
   ```

3. **Accéder à l'application** :
   - **API Documentation (Swagger)** : http://localhost:8000/swagger/
   - **Page d'accueil** : http://localhost:8000/ (redirige vers Swagger)
   - **Interface Web** : 
     - Rapport des ventes : http://localhost:8000/uc1/rapport/
     - Gestion du stock : http://localhost:8000/uc2/stock/
     - Dashboard performances : http://localhost:8000/uc3/dashboard/
     - Gestion des produits : http://localhost:8000/uc4/produits/

---

## API REST - Endpoints disponibles

L'API est versionnée et accessible sous `/api/v1/`. Authentification par token requis pour certains endpoints.

### Authentification
```bash
# Header requis pour les endpoints sécurisés
Authorization: Token token-430
```

### Endpoints principaux

| Endpoint | Méthode | Description | Auth |
|----------|---------|-------------|------|
| `/api/v1/reports/` | GET | Rapport consolidé des ventes | Non |
| `/api/v1/stores/{id}/stock/` | GET | Stock d'un magasin spécifique | Non |
| `/api/v1/stores/{id}/stock/list/` | GET | Liste paginée du stock (tri/filtrage) | Non |
| `/api/v1/dashboard/` | GET | Performances globales des magasins | Non |
| `/api/v1/products/{id}/` | GET | Informations d'un produit | Non |
| `/api/v1/products/{id}/` | PUT | Mise à jour d'un produit | **Oui** |

### Exemple d'utilisation

```bash
# Consulter le rapport des ventes
curl -X GET http://localhost:8000/api/v1/reports/

# Stock simple d'un magasin
curl -X GET http://localhost:8000/api/v1/stores/1/stock/

# Stock paginé avec filtrage et tri
curl -X GET "http://localhost:8000/api/v1/stores/1/stock/list/?page=1&produit__nom=Café&ordering=-quantite"

# Mettre à jour un produit (avec authentification)
curl -X PUT http://localhost:8000/api/v1/products/1/ \
  -H "Authorization: Token token-430" \
  -H "Content-Type: application/json" \
  -d '{"nom": "Nouveau nom", "prix": 15.99}'
```

### Pagination, filtrage et tri

L'endpoint `/api/v1/stores/{id}/stock/list/` supporte :

- **Pagination** : `?page=2` (10 éléments par page par défaut)
- **Filtrage** : 
  - `?produit__nom=Café` (filtrer par nom de produit - recherche partielle)
  - `?quantite=5` (filtrer par quantité exacte)
- **Tri** : 
  - `?ordering=quantite` (tri croissant par quantité)
  - `?ordering=-quantite` (tri décroissant par quantité)
  - `?ordering=produit__nom` (tri par nom de produit)

### Format de réponse enrichi

Les réponses incluent les informations détaillées :
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/v1/stores/1/stock/list/?page=2",
  "previous": null,
  "results": [
    {
      "id": 4,
      "produit": 4,
      "magasin": 1,
      "quantite": 30,
      "produit_nom": "Café Premium Bio",
      "magasin_nom": "Magasin Centre-Ville"
    }
  ]
}
```

Exemples d'utilisation :
```bash
# Page 2, produits contenant "Café", triés par quantité décroissante
curl "http://localhost:8000/api/v1/stores/1/stock/list/?page=2&produit__nom=Café&ordering=-quantite"

# Filtrer par quantité exacte
curl "http://localhost:8000/api/v1/stores/1/stock/list/?quantite=5"

# Tri par nom de produit
curl "http://localhost:8000/api/v1/stores/1/stock/list/?ordering=produit__nom"
```

---

## Fonctionnalités implémentées

### Cas d'utilisation couverts

- **UC1 - Rapport des ventes** : Génération de rapports consolidés par magasin
- **UC2 - Gestion du stock** : Consultation des stocks et demandes de réapprovisionnement
- **UC3 - Performances** : Tableau de bord avec indicateurs clés (CA, ruptures, tendances)
- **UC4 - Gestion des produits** : CRUD complet des produits avec validation
  
### Fonctionnalités techniques

- **API REST** avec Django REST Framework
- **Pagination automatique** (10 éléments par page)
- **Filtrage avancé** par attributs (nom, quantité, relations)
- **Tri multi-critères** (croissant/décroissant)
- **Documentation automatique** avec Swagger/OpenAPI
- **Authentification par token** pour les opérations sensibles
- **CORS configuré** pour les clients externes
- **Validation des données** avec des sérialiseurs
- **Gestion d'erreurs normalisées** (format JSON standard)
- **Tests d'API automatisés** avec pytest
- **Séparation des couches** (Présentation, Services, Domaine)
- **Formatage de code** avec Black et configuration pylint-django

---

## Tests

### Exécution des tests

```bash
# Tous les tests
docker-compose run --rm web-labo3 pytest

# Tests spécifiques à l'API
docker-compose run --rm web-labo3 pytest magasin/api/tests/

```

### Types de tests

- **Tests unitaires** : Logique métier des services
- **Tests d'intégration** : Interaction entre les couches
- **Tests d'API** : Endpoints REST (codes de statut, format JSON)
- **Tests de pagination/filtrage** : Fonctionnalités avancées de l'API
- **Tests end-to-end** : Scénarios complets utilisateur

### Exécution avec différentes bases de données

```bash
# Tests avec PostgreSQL (recommandé - production-like)
DB_HOST=localhost python -m pytest magasin/api/tests/ -v

# Tests locaux en développement
docker-compose run --rm web-labo3 pytest magasin/api/tests/
```

---

## Architecture

Le projet suit une **architecture en couches** :

1. **Couche Présentation** : 
   - Web (vues Django + templates)
   - API (contrôleurs REST + sérialiseurs)

2. **Couche Services** : 
   - Logique métier centralisée et réutilisable

3. **Couche Domaine** : 
   - Modèles de données (ORM Django)

Cette séparation permet d'exposer la même logique métier via deux interfaces différentes sans duplication de code.

---

## Technologies utilisées

| Composant | Technologie | Justification |
|-----------|-------------|---------------|
| **Framework Web** | Django 4.x | Framework mature et robuste |
| **API REST** | Django REST Framework | Standard de facto pour les APIs Django |
| **Documentation API** | drf-yasg (Swagger) | Génération automatique de documentation |
| **Base de données** | PostgreSQL | Robustesse et performance |
| **Filtrage/Pagination** | django-filter + DRF | APIs riches avec tri et filtrage |
| **Conteneurisation** | Docker + Docker Compose | Environnement reproductible |
| **Tests** | pytest + pytest-django | Framework de tests moderne |
| **Authentification** | Token-based Auth | Simple et efficace pour les APIs |
| **Formatage code** | Black + pylint-django | Code cohérent et qualité |

---

## Développement

### Structure des services

Chaque cas d'utilisation a son service dédié dans `magasin/services/` :
- Logique métier centralisée
- Réutilisable par les vues web et API
- Facilite les tests unitaires

### Ajout d'un nouvel endpoint

1. Créer le service dans `magasin/services/`
2. Créer le contrôleur dans `magasin/api/controllers/`
3. Créer le sérialiseur dans `magasin/api/serializers/`
4. Ajouter la route dans `magasin/api/urls.py`
5. Écrire les tests dans `magasin/api/tests/`

---

Voici un exemple de pipeline : https://github.com/TalipKoyluoglu/LOG430-Labo3/actions/runs/15809245599

--- 

## Auteur

Projet réalisé par Talip Koyluoglu.
