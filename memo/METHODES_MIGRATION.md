# Méthodes de Migration de Modèles Django

## Contexte

Pour la refactorisation de l'application `oc_lettings_site` en deux applications distinctes (`lettings` et `profiles`), il existe trois approches principales pour déplacer les modèles Django.

---

## 1. La Méthode Longue (The Long Way) - Copie des données

### Description
Cette méthode consiste à créer un nouveau modèle dans la nouvelle application, copier toutes les données de l'ancien modèle vers le nouveau, mettre à jour les clés étrangères, puis supprimer l'ancien modèle.

### Étapes
1. Créer le nouveau modèle dans la nouvelle application
2. Générer et exécuter les migrations pour créer la nouvelle table
3. Copier les données de l'ancienne table vers la nouvelle (via `RunPython`)
4. Mettre à jour les clés étrangères pour pointer vers le nouveau modèle
5. Supprimer l'ancien modèle

### Avantages
- **Sécurité maximale** : Les données sont copiées, pas déplacées
- **Réversibilité** : Facile à annuler car l'ancienne table existe encore temporairement
- **Clarté** : Chaque étape est explicite et compréhensible
- **Compatibilité** : Fonctionne avec tous les types de bases de données

### Inconvénients
- **Lenteur** : Peut être très long pour les grandes tables
- **Espace disque** : Nécessite temporairement le double d'espace
- **Complexité** : Nombreuses migrations à gérer
- **Temps d'arrêt** : Potentiellement long pour les bases volumineuses

---

## 2. La Méthode Rapide (The Short Way) - Référence à l'ancienne table

### Description
Cette méthode consiste à créer un nouveau modèle qui pointe vers l'ancienne table en utilisant l'option `db_table` dans la classe `Meta`. Aucune donnée n'est déplacée.

### Étapes
1. Créer le nouveau modèle avec `class Meta: db_table = 'ancien_nom_table'`
2. Supprimer l'ancien modèle du code
3. Utiliser `SeparateDatabaseAndState` pour synchroniser l'état Django sans toucher à la base de données

### Avantages
- **Rapidité** : Aucune copie de données, exécution quasi instantanée
- **Simplicité** : Moins de migrations à écrire
- **Pas de temps d'arrêt** : La base de données n'est pas modifiée

### Inconvénients
- **Nom de table incohérent** : La table garde son ancien nom (ex: `catalog_product` au lieu de `product_product`)
- **Confusion potentielle** : Le nom de la table ne correspond plus à l'application
- **Dette technique** : Laisse des traces de l'ancienne architecture
- **Maintenance** : Peut compliquer la compréhension du schéma pour les nouveaux développeurs

---

## 3. La Méthode Django (The Django Way) - Renommage de table

### Description
Cette méthode utilise les opérations de migration Django pour renommer la table de base de données afin qu'elle corresponde au nouveau modèle, tout en utilisant `SeparateDatabaseAndState` pour gérer séparément l'état Django et les opérations sur la base de données.

### Étapes
1. Créer le nouveau modèle dans la nouvelle application
2. Générer les migrations automatiques
3. Modifier manuellement les migrations pour utiliser `SeparateDatabaseAndState`
4. Utiliser `AlterModelTable` pour renommer la table
5. Mettre à jour les contraintes et index

### Avantages
- **Cohérence** : Le nom de la table correspond à la nouvelle application
- **Performance** : Renommer une table est très rapide
- **Propreté** : Pas de dette technique, architecture propre
- **Standard Django** : Utilise les mécanismes natifs de Django

### Inconvénients
- **Complexité** : Nécessite une bonne compréhension des migrations Django
- **Modifications manuelles** : Les migrations générées doivent être éditées
- **Risque d'erreur** : Une mauvaise manipulation peut corrompre l'état
- **Débogage difficile** : Plus complexe à diagnostiquer en cas de problème

---

## Recommandation pour le Projet OC Lettings

### Mon choix : La Méthode Django (The Django Way)

### Justification

1. **Cohérence architecturale** : Le projet est une refactorisation complète visant à améliorer la modularité. Il est logique que les noms de tables reflètent la nouvelle architecture (`lettings_address`, `lettings_letting`, `profiles_profile`).

2. **Taille des données** : Pour un projet d'apprentissage/démonstration, les volumes de données sont faibles. La performance n'est pas un critère décisif, mais la méthode Django reste performante.

3. **Objectif pédagogique** : OpenClassrooms vise l'apprentissage des bonnes pratiques Django. La méthode Django est la plus "propre" et enseigne les concepts avancés de migration.

4. **Exigences du projet** : Le cahier des charges mentionne explicitement :
   - "Remplir les nouvelles tables avec les données déjà présentes en utilisant les fichiers de migration Django"
   - "Ne pas utiliser le langage SQL directement"
   - "Supprimer les anciennes tables de la base de données"

   Ces exigences correspondent parfaitement à la méthode Django.

5. **Maintenabilité future** : Une architecture propre avec des noms de tables cohérents facilitera la maintenance et l'évolution du projet.

6. **Pas de dette technique** : Contrairement à la méthode rapide, on ne laisse pas de traces de l'ancienne architecture.

### Alternative acceptable : La Méthode Longue

Si la complexité de la méthode Django pose problème, la méthode longue reste une alternative valable car elle :
- Répond aux exigences de migration des données via Django
- Permet de supprimer proprement les anciennes tables
- Est plus facile à comprendre et déboguer

---

## Tableau Comparatif

| Critère | Méthode Longue | Méthode Rapide | Méthode Django |
|---------|----------------|----------------|----------------|
| Complexité | Moyenne | Faible | Élevée |
| Performance | Lente | Très rapide | Rapide |
| Cohérence des noms | ✅ Oui | ❌ Non | ✅ Oui |
| Réversibilité | ✅ Facile | ⚠️ Moyenne | ⚠️ Moyenne |
| Dette technique | ❌ Non | ⚠️ Oui | ❌ Non |
| Conforme aux exigences OC | ✅ Oui | ❌ Non | ✅ Oui |

---

## Conclusion

**La méthode Django est recommandée** pour ce projet car elle offre le meilleur équilibre entre propreté architecturale, conformité aux exigences du projet, et valeur pédagogique. Elle permet d'obtenir une base de données avec des noms de tables cohérents tout en utilisant les mécanismes natifs de Django.

## Source

- [How to Move a Django Model to Another App - Real Python](https://realpython.com/move-django-model/)
