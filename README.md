# AuditMatch — Outil de rapprochement Excel

## Installation (une seule fois)

```bash
pip install streamlit pandas openpyxl plotly
```

## Lancer l'application

```bash
streamlit run audit_app.py
```

Une page va s'ouvrir automatiquement dans ton navigateur à l'adresse `http://localhost:8501`.

## Utilisation

1. Importer les deux fichiers Excel (ou CSV) à comparer.
2. Choisir la colonne clé (identifiant unique, ex : n° de facture) et la colonne montant.
3. Ajuster la tolérance d'écart si besoin (par défaut 0,01 €).
4. Cliquer sur "Lancer le rapprochement".
5. Consulter le dashboard et télécharger le rapport Excel complet.

## Fichiers d'exemple

`exemple_grand_livre.xlsx` et `exemple_releve.xlsx` sont fournis pour tester l'app immédiatement — ils contiennent volontairement quelques écarts et lignes manquantes.
