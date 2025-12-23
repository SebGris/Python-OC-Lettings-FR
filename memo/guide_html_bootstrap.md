# Guide des Templates HTML et Classes Bootstrap

Ce document explique le code HTML et les classes CSS (Bootstrap 5) utilisées dans les templates du projet OC Lettings.

---

## Table des matieres

1. [Structure generale des templates](#structure-generale-des-templates)
2. [Classes Bootstrap - Espacement](#classes-bootstrap---espacement)
3. [Classes Bootstrap - Typographie](#classes-bootstrap---typographie)
4. [Classes Bootstrap - Layout et Grille](#classes-bootstrap---layout-et-grille)
5. [Classes Bootstrap - Composants](#classes-bootstrap---composants)
6. [Tags Django Template](#tags-django-template)
7. [Reference par fichier](#reference-par-fichier)

---

## Structure generale des templates

Le projet utilise le systeme d'heritage de templates Django avec un fichier `base.html` qui definit la structure commune.

### Balises HTML de base

| Balise | Description |
|--------|-------------|
| `<!DOCTYPE html>` | Declaration du type de document HTML5 |
| `<html lang="en">` | Element racine avec attribut de langue |
| `<head>` | Contient les metadonnees (titre, CSS, scripts) |
| `<body>` | Contient le contenu visible de la page |
| `<main>` | Contenu principal de la page |
| `<nav>` | Barre de navigation |
| `<footer>` | Pied de page |
| `<div>` | Conteneur generique |
| `<h1>`, `<h2>` | Titres (niveaux 1 et 2) |
| `<p>` | Paragraphe |
| `<a>` | Lien hypertexte |
| `<ul>`, `<li>` | Liste non ordonnee et ses elements |
| `<hr>` | Ligne horizontale de separation |
| `<img>` | Image |
| `<i>` | Icone (utilise avec Feather Icons) |

---

## Classes Bootstrap - Espacement

Bootstrap utilise un systeme de classes utilitaires pour gerer les marges et paddings.

### Syntaxe : `{propriete}{cote}-{taille}`

**Proprietes :**
- `m` = margin (marge externe)
- `p` = padding (marge interne)

**Cotes :**
- `t` = top (haut)
- `b` = bottom (bas)
- `s` = start/left (gauche)
- `e` = end/right (droite)
- `x` = horizontal (gauche et droite)
- `y` = vertical (haut et bas)
- (rien) = tous les cotes

**Tailles :**
- `0` = 0
- `1` = 0.25rem
- `2` = 0.5rem
- `3` = 1rem (16px)
- `4` = 1.5rem
- `5` = 3rem
- `auto` = automatique

### Classes d'espacement utilisees dans le projet

| Classe | Signification | Effet |
|--------|---------------|-------|
| `mb-3` | margin-bottom: 3 | Marge en bas de 1rem (16px) |
| `mb-4` | margin-bottom: 4 | Marge en bas de 1.5rem (24px) |
| `mb-0` | margin-bottom: 0 | Aucune marge en bas |
| `mt-auto` | margin-top: auto | Marge haute automatique (pousse l'element vers le bas) |
| `my-5` | margin-y: 5 | Marge verticale de 3rem |
| `m-0` | margin: 0 | Aucune marge |
| `px-5` | padding-x: 5 | Padding horizontal de 3rem |
| `px-10` | padding-x: 10 | Padding horizontal etendu (classe personnalisee) |
| `py-5` | padding-y: 5 | Padding vertical de 3rem |
| `pb-5` | padding-bottom: 5 | Padding en bas de 3rem |
| `ms-lg-4` | margin-start-lg: 4 | Marge gauche de 1.5rem sur ecrans larges (>= 992px) |
| `ms-2` | margin-start: 2 | Marge gauche de 0.5rem |

---

## Classes Bootstrap - Typographie

### Classes d'affichage (Display)

| Classe | Description | Utilisation |
|--------|-------------|-------------|
| `display-1` | Titre tres grand | Code d'erreur 404/500 |
| `display-6` | Titre moyen | Sous-titres des pages |

**Exemple dans le code :**
```html
<h1 class="page-header-ui-title mb-3 display-1">404</h1>
<h2 class="mb-3 display-6">Page Not Found</h2>
```

### Autres classes de texte

| Classe | Description |
|--------|-------------|
| `text-center` | Centre le texte horizontalement |
| `text-white` | Texte en blanc |
| `text-md-end` | Texte aligne a droite sur ecrans moyens+ |
| `fw-500` | Font-weight 500 (semi-gras, classe personnalisee) |
| `small` | Texte plus petit |

---

## Classes Bootstrap - Layout et Grille

### Conteneurs

| Classe | Description |
|--------|-------------|
| `container` | Conteneur avec largeur maximale responsive |

### Systeme de grille

Bootstrap utilise un systeme de grille a 12 colonnes.

| Classe | Description |
|--------|-------------|
| `row` | Cree une ligne de grille (flexbox) |
| `col-lg-8` | Colonne de 8/12 (66.67%) sur grands ecrans |
| `col-lg-10` | Colonne de 10/12 (83.33%) sur grands ecrans |
| `col-md-6` | Colonne de 6/12 (50%) sur ecrans moyens |
| `gx-5` | Gouttiere horizontale de taille 5 entre colonnes |

### Classes Flexbox

| Classe | Description |
|--------|-------------|
| `justify-content-center` | Centre les elements horizontalement |
| `align-items-center` | Centre les elements verticalement |

---

## Classes Bootstrap - Composants

### Navbar (Barre de navigation)

| Classe | Description |
|--------|-------------|
| `navbar` | Composant de navigation |
| `navbar-expand-lg` | S'etend sur grands ecrans, collapse sur petits |
| `navbar-light` | Style clair (texte sombre) |
| `navbar-brand` | Logo/nom du site |
| `bg-white` | Fond blanc |

### Boutons

| Classe | Description |
|--------|-------------|
| `btn` | Style de base d'un bouton |
| `btn-primary` | Bouton avec couleur primaire (bleu) |

**Exemple :**
```html
<a class="btn fw-500 ms-lg-4 btn-primary px-10" href="...">
    Profiles
</a>
```

### Cartes (Cards)

| Classe | Description |
|--------|-------------|
| `card` | Conteneur de carte |
| `card-body` | Corps de la carte |

### Listes

| Classe | Description |
|--------|-------------|
| `list-group` | Groupe de liste |
| `list-group-flush` | Liste sans bordures laterales |
| `list-group-item` | Element de liste |
| `list-group-careers` | Style personnalise |

### Footer

| Classe | Description |
|--------|-------------|
| `footer` | Pied de page |
| `footer-dark` | Style sombre pour le footer |
| `bg-dark` | Fond sombre |

### Icones

| Classe | Description |
|--------|-------------|
| `icon-stack` | Conteneur d'icone empilee |
| `icon-stack-lg` | Grande taille |
| `bg-primary` | Fond couleur primaire |

**Utilisation avec Feather Icons :**
```html
<i data-feather="home"></i>
<i data-feather="user"></i>
<i data-feather="arrow-left"></i>
<i data-feather="arrow-right"></i>
```

---

## Tags Django Template

### Heritage de templates

| Tag | Description |
|-----|-------------|
| `{% extends "base.html" %}` | Herite du template de base |
| `{% block title %}...{% endblock %}` | Definit le contenu du bloc titre |
| `{% block content %}...{% endblock %}` | Definit le contenu principal |

### Fichiers statiques

| Tag | Description |
|-----|-------------|
| `{% load static %}` | Charge le module des fichiers statiques |
| `{% static 'chemin/fichier' %}` | Genere l'URL d'un fichier statique |

**Exemple :**
```html
<link href="{% static 'css/styles.css' %}" rel="stylesheet" />
<img src="{% static 'assets/img/logo.png' %}" />
```

### URLs

| Tag | Description |
|-----|-------------|
| `{% url 'nom_route' %}` | Genere l'URL d'une route |
| `{% url 'app:route' param=valeur %}` | Route avec namespace et parametre |

**Exemples :**
```html
<a href="{% url 'index' %}">Home</a>
<a href="{% url 'profiles:index' %}">Profiles</a>
<a href="{% url 'lettings:letting' letting_id=letting.id %}">{{ letting.title }}</a>
```

### Boucles et conditions

| Tag | Description |
|-----|-------------|
| `{% if condition %}` | Condition |
| `{% else %}` | Sinon |
| `{% endif %}` | Fin de condition |
| `{% for item in liste %}` | Boucle |
| `{% endfor %}` | Fin de boucle |

**Exemple :**
```html
{% if lettings_list %}
    <ul>
        {% for letting in lettings_list %}
            <li>{{ letting.title }}</li>
        {% endfor %}
    </ul>
{% else %}
    <p>No lettings are available.</p>
{% endif %}
```

### Variables

| Syntaxe | Description |
|---------|-------------|
| `{{ variable }}` | Affiche la valeur d'une variable |
| `{{ objet.attribut }}` | Accede a un attribut d'objet |

---

## Reference par fichier

### base.html

Template de base qui definit :
- Structure HTML complete (head, body)
- Chargement des CSS et JS (Bootstrap, AOS, Font Awesome, Feather Icons)
- Navbar avec liens vers Profiles et Lettings
- Footer avec copyright
- Blocs `title` et `content` pour l'heritage

**Classes principales utilisees :**
- `navbar navbar-expand-lg bg-white navbar-light`
- `container`
- `navbar-brand`
- `btn fw-500 ms-lg-4 btn-primary`
- `footer pb-5 mt-auto bg-dark footer-dark`

### index.html (Accueil)

**Structure :**
```
container > row > col-lg-8 > h1 (titre)
container > boutons (Profiles, Lettings)
```

**Classes cles :**
- `container px-5 py-5 text-center`
- `row justify-content-center`
- `col-lg-8`
- `page-header-ui-title mb-3 display-6`

### 404.html et 500.html (Pages d'erreur)

**Structure identique :**
```
container > row > col-lg-8 > h1 (code erreur) + h2 (message) + p (description)
container > bouton retour
```

**Classes cles :**
- `display-1` pour le code d'erreur (404/500)
- `display-6` pour le sous-titre
- `mb-3`, `mb-4` pour l'espacement

### lettings/index.html et profiles/index.html

**Structure :**
```
container > row > col-lg-8 > h1 (titre)
container > row > col-lg-10 > liste des elements
container > boutons navigation
```

**Classes cles :**
- `list-group list-group-flush list-group-careers`
- `list-group-item`

### letting.html et profile.html (Details)

**Structure :**
```
container > row > col-lg-8 > h1 (titre)
container > card > card-body > informations
container > boutons navigation
```

**Classes cles :**
- `card`, `card-body`
- `icon-stack icon-stack-lg bg-primary text-white mb-3`

---

## Resume des classes les plus utilisees

| Classe | Frequence | Role |
|--------|-----------|------|
| `container` | Tres haute | Conteneur principal |
| `px-5 py-5` | Haute | Espacement standard des sections |
| `text-center` | Haute | Centrage du texte |
| `row` | Haute | Ligne de grille |
| `justify-content-center` | Haute | Centrage horizontal |
| `col-lg-8` | Moyenne | Colonne de contenu |
| `btn btn-primary` | Haute | Boutons de navigation |
| `mb-3` | Haute | Marge inferieure standard |
| `display-6` | Moyenne | Taille des titres |

---

## Ressources externes

- [Documentation Bootstrap 5](https://getbootstrap.com/docs/5.1/)
- [Feather Icons](https://feathericons.com/)
- [AOS - Animate On Scroll](https://michalsnik.github.io/aos/)
- [Font Awesome](https://fontawesome.com/)
- [Django Templates](https://docs.djangoproject.com/en/4.2/ref/templates/language/)
