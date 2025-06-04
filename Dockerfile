# Étape 1 : image de base Python légère
FROM python:3.12-slim

# Étape 2 : définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : copier le projet complet dans le conteneur
COPY . .

# Étape 4 : installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Ajout du PYTHONPATH pour permettre les imports relatifs
ENV PYTHONPATH=/app/src

# Étape 5 : exécuter le point d’entrée console
CMD ["python", "src/main.py"]
