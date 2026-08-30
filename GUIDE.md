# Guide de test — AuditMatch (v0)

Salut ! Voici comment tester l'outil et donner ton avis. Ça prend environ 5 minutes.

---

## Ce que fait l'outil

AuditMatch compare deux fichiers Excel (ou CSV) ligne par ligne, à partir d'une colonne
identifiant (ex : n° de facture). Il repère automatiquement :

- les lignes qui correspondent parfaitement entre les deux fichiers
- les lignes qui existent dans les deux fichiers mais avec un montant différent (un écart)
- les lignes présentes dans un seul des deux fichiers

L'idée : remplacer un rapprochement fait manuellement dans Excel par quelque chose
d'automatique et visuel.

---

## Étape 1 — Importer les fichiers

En haut de la page, deux zones d'import :

- **Fichier de référence** (à gauche) — par exemple ton grand livre
- **Fichier à comparer** (à droite) — par exemple un relevé bancaire

Glisse-dépose un fichier Excel (.xlsx) ou CSV dans chaque zone, ou clique sur
"Upload" pour aller le chercher sur ton ordinateur.

> Pas de fichiers réels sous la main ? Deux fichiers d'exemple sont fournis
> (`exemple_grand_livre.xlsx` et `exemple_releve.xlsx`) — ils contiennent volontairement
> quelques écarts et lignes manquantes, pour voir le rendu tout de suite.

---

## Étape 2 — Configurer le rapprochement

Une fois les deux fichiers importés, trois réglages apparaissent :

| Réglage | À quoi ça sert |
|---|---|
| **Colonne(s) clé** | La colonne qui identifie une ligne de façon unique dans les deux fichiers (ex : n° de facture, référence). C'est sur cette colonne que les deux fichiers sont mis en correspondance. |
| **Colonne montant** | La colonne numérique à comparer entre les deux fichiers. |
| **Tolérance d'écart** | En dessous de ce seuil (en €), un écart n'est pas considéré comme une anomalie — utile pour ignorer les arrondis. |

---

## Étape 3 — Lancer et lire les résultats

Clique sur **"Lancer le rapprochement"**. Le tableau de bord affiche :

- **3 indicateurs** en haut : lignes rapprochées, écarts détectés (avec le détail
  majeurs/mineurs), et un score de cohérence sur 100
- **Un résumé en une phrase** qui pointe l'écart le plus important
- **Un graphique** des plus gros écarts, et **une répartition** en donut
- **Un tableau détaillé** des lignes en écart, avec un badge de sévérité
- **Les lignes présentes dans un seul fichier**, dans des onglets séparés
- Un **bouton de téléchargement** pour récupérer un rapport Excel complet

---

## Étape 4 — Donner ton avis

C'est la partie la plus utile pour la suite. Prends 2 minutes pour noter :

- **Ce qui te semble déjà utile** tel quel
- **Ce qui manque** — un filtre, une colonne en plus, un autre type de rapprochement ?
- **Ce qui te dérange visuellement** — trop chargé, pas assez clair, mal nommé ?
- **Le cas d'usage réel** que ça pourrait couvrir dans ton travail au quotidien

N'hésite pas à tester avec un vrai fichier à toi (anonymisé si besoin) pour voir si
l'outil tient la route sur des données réelles, pas seulement sur l'exemple.

---

## Un souci technique ?

Si la page semble figée (impossible de cliquer ou de faire défiler) :

1. Ferme complètement l'onglet du navigateur
2. Dans le terminal, arrête le serveur (`Ctrl + C`)
3. Relance `streamlit run audit_app.py`
4. Rouvre un nouvel onglet

Sinon, note simplement ce qui a coincé — c'est aussi un retour utile.