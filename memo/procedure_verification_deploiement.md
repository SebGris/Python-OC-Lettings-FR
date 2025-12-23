# Procedure de verification du deploiement

Ce document decrit la procedure pour verifier que le pipeline CI/CD fonctionne correctement en modifiant le titre de la page d'accueil, en redeployant le site, et en extrayant l'image Docker depuis Docker Hub.

---

## Table des matieres

1. [Prerequis](#1-prerequis)
2. [Etape 1 : Modifier le titre de la page d'accueil](#2-etape-1--modifier-le-titre-de-la-page-daccueil)
3. [Etape 2 : Commit et push des modifications](#3-etape-2--commit-et-push-des-modifications)
4. [Etape 3 : Verifier le pipeline CI/CD](#4-etape-3--verifier-le-pipeline-cicd)
5. [Etape 4 : Verifier le deploiement sur Render](#5-etape-4--verifier-le-deploiement-sur-render)
6. [Etape 5 : Extraire l'image Docker depuis Docker Hub](#6-etape-5--extraire-limage-docker-depuis-docker-hub)
7. [Etape 6 : Executer l'image Docker localement](#7-etape-6--executer-limage-docker-localement)
8. [Resume du flux complet](#8-resume-du-flux-complet)

---

## 1. Prerequis

Avant de commencer, assurez-vous d'avoir :

| Element | Description |
|---------|-------------|
| Git | Installe et configure |
| Docker Desktop | Installe et en cours d'execution |
| Acces GitHub | Droits de push sur le repository |
| Compte Docker Hub | Pour extraire l'image |

### Verifier les installations

```bash
# Verifier Git
git --version

# Verifier Docker
docker --version

# Verifier que Docker est en cours d'execution
docker info
```

---

## 2. Etape 1 : Modifier le titre de la page d'accueil

### Fichier a modifier

Le fichier de la page d'accueil est : `templates/index.html`

### Contenu actuel

```html
{% extends "base.html" %}
{% block title %}Holiday Homes{% endblock title %}

{% block content %}

<div class="container px-5 py-5 text-center">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <h1 class="page-header-ui-title mb-3 display-6">Welcome to Holiday Homes</h1>
        </div>
    </div>
</div>
...
{% endblock %}
```

### Modification a effectuer

Modifier le titre `<h1>` (ligne 10) :

**Avant :**
```html
<h1 class="page-header-ui-title mb-3 display-6">Welcome to Holiday Homes</h1>
```

**Apres (exemple) :**
```html
<h1 class="page-header-ui-title mb-3 display-6">Bienvenue sur OC Lettings</h1>
```

Vous pouvez egalement modifier le `<title>` dans le bloc title (ligne 2) :

**Avant :**
```html
{% block title %}Holiday Homes{% endblock title %}
```

**Apres :**
```html
{% block title %}OC Lettings - Accueil{% endblock title %}
```

---

## 3. Etape 2 : Commit et push des modifications

### Verifier les modifications

```bash
# Voir les fichiers modifies
git status

# Voir le detail des modifications
git diff templates/index.html
```

### Creer le commit

```bash
# Ajouter le fichier modifie
git add templates/index.html

# Creer le commit avec un message descriptif
git commit -m "Modification du titre de la page d'accueil"
```

### Pousser vers GitHub

```bash
# Pousser sur la branche master
git push origin master
```

---

## 4. Etape 3 : Verifier le pipeline CI/CD

### Acces au pipeline GitHub Actions

1. Aller sur le repository GitHub
2. Cliquer sur l'onglet **Actions**
3. Observer le workflow **CI/CD Pipeline** qui s'execute

### Les 3 jobs du pipeline

| Job | Description | Condition |
|-----|-------------|-----------|
| **Tests & Linting** | Execute flake8 et pytest | Toujours |
| **Build & Push Docker Image** | Construit et pousse l'image sur Docker Hub | Si tests OK + branche master |
| **Deploy to Render** | Declenche le deploiement via webhook | Si build OK + branche master |

### Verifier le succes

- Tous les jobs doivent afficher une coche verte
- En cas d'erreur, cliquer sur le job pour voir les logs

### Temps d'execution estime

- Tests : ~1-2 minutes
- Build Docker : ~2-3 minutes
- Deploy : ~1-2 minutes
- **Total : ~5-7 minutes**

---

## 5. Etape 4 : Verifier le deploiement sur Render

### URL de l'application

Acceder a l'application deployee :
```
https://python-oc-lettings-fr-sg.onrender.com
```

*(Remplacez par votre URL Render si differente)*

### Verification

1. Ouvrir l'URL dans un navigateur
2. Verifier que le nouveau titre s'affiche sur la page d'accueil
3. Verifier que l'onglet du navigateur affiche le nouveau titre

### En cas de probleme

- Verifier les logs sur le dashboard Render
- S'assurer que le webhook de deploiement a ete declenche
- Attendre quelques minutes (le deploiement peut prendre du temps)

---

## 6. Etape 5 : Extraire l'image Docker depuis Docker Hub

### Informations de l'image

| Element | Valeur |
|---------|--------|
| Registry | Docker Hub |
| Image | `<votre-username>/oc-lettings` |
| Tags disponibles | `latest`, `<sha-du-commit>` |

### Commande pour extraire l'image

```bash
# Extraire la derniere version (tag latest)
docker pull <votre-username>/oc-lettings:latest

# Ou extraire une version specifique avec le SHA du commit
docker pull <votre-username>/oc-lettings:<sha-commit>
```

### Exemple concret

```bash
# Remplacez 'monusername' par votre username Docker Hub
docker pull monusername/oc-lettings:latest
```

### Verifier que l'image est telechargee

```bash
# Lister les images Docker locales
docker images | grep oc-lettings
```

**Resultat attendu :**
```
monusername/oc-lettings   latest    abc123def456   2 hours ago   150MB
```

---

## 7. Etape 6 : Executer l'image Docker localement

### Lancer le conteneur

```bash
# Executer l'image en mode detache
docker run -d \
  --name oc-lettings-local \
  -p 8000:8000 \
  -e SECRET_KEY="votre-secret-key-locale" \
  -e DEBUG="True" \
  <votre-username>/oc-lettings:latest
```

### Explication des options

| Option | Description |
|--------|-------------|
| `-d` | Mode detache (en arriere-plan) |
| `--name oc-lettings-local` | Nom du conteneur |
| `-p 8000:8000` | Mapping du port 8000 |
| `-e SECRET_KEY="..."` | Variable d'environnement |
| `-e DEBUG="True"` | Active le mode debug |

### Verifier que le conteneur fonctionne

```bash
# Voir les conteneurs en cours d'execution
docker ps

# Voir les logs du conteneur
docker logs oc-lettings-local
```

### Acceder a l'application locale

Ouvrir dans un navigateur :
```
http://localhost:8000
```

### Verifier la modification

- Le nouveau titre doit s'afficher sur la page d'accueil
- Cela confirme que l'image Docker contient bien les modifications

### Arreter et supprimer le conteneur

```bash
# Arreter le conteneur
docker stop oc-lettings-local

# Supprimer le conteneur
docker rm oc-lettings-local
```

---

## 8. Resume du flux complet

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROCEDURE DE VERIFICATION                             │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │ 1. MODIFIER │  Editer templates/index.html
    │    LE CODE  │  Changer le titre <h1>
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ 2. COMMIT   │  git add templates/index.html
    │    & PUSH   │  git commit -m "..."
    │             │  git push origin master
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ 3. PIPELINE │  GitHub Actions s'execute automatiquement :
    │    CI/CD    │  - Tests & Linting
    │             │  - Build Docker Image
    │             │  - Push vers Docker Hub
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ 4. DEPLOY   │  Webhook declenche Render
    │    RENDER   │  Application mise a jour
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ 5. VERIFIER │  Acceder a l'URL Render
    │    EN LIGNE │  Confirmer le nouveau titre
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ 6. DOCKER   │  docker pull <user>/oc-lettings:latest
    │    PULL     │  docker run -d -p 8000:8000 ...
    │             │  Verifier sur http://localhost:8000
    └─────────────┘
```

---

## Commandes resumees

```bash
# 1. Modifier le fichier (avec votre editeur)
code templates/index.html

# 2. Commit et push
git add templates/index.html
git commit -m "Modification du titre de la page d'accueil"
git push origin master

# 3. Attendre le pipeline (verifier sur GitHub Actions)

# 4. Verifier le deploiement (ouvrir l'URL Render)

# 5. Extraire l'image Docker
docker pull <votre-username>/oc-lettings:latest

# 6. Executer localement
docker run -d --name oc-lettings-local -p 8000:8000 \
  -e SECRET_KEY="test-key" -e DEBUG="True" \
  <votre-username>/oc-lettings:latest

# 7. Verifier sur http://localhost:8000

# 8. Nettoyer
docker stop oc-lettings-local && docker rm oc-lettings-local
```

---

## Depannage

### Le pipeline echoue

| Probleme | Solution |
|----------|----------|
| Tests echouent | Verifier les logs, corriger le code, repousser |
| Build Docker echoue | Verifier le Dockerfile et les secrets GitHub |
| Deploy echoue | Verifier le webhook Render dans les secrets |

### L'image Docker ne se telecharge pas

```bash
# Se connecter a Docker Hub
docker login

# Reessayer le pull
docker pull <votre-username>/oc-lettings:latest
```

### Le conteneur ne demarre pas

```bash
# Voir les logs d'erreur
docker logs oc-lettings-local

# Verifier les variables d'environnement requises
```
