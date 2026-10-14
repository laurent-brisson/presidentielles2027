# Présidentielle 2027

Données ouvertes sur les candidats à l'élection présidentielle française de 2027
(premier tour le 18 avril 2027, second tour le 2 mai 2027). Objectif à terme :
un outil d'exploration des promesses de campagne.

## Contenu

| Fichier | Rôle |
|---|---|
| `data/candidates.yaml` | Candidats déclarés (fiche standardisée, sources, statut) |
| `data/parties.yaml` | Partis et mouvements, référencés par identifiant |
| `data/watchlist.yaml` | Personnalités pressenties ou déclarations non confirmées |
| `schema/candidates.schema.json` | Schéma JSON de validation |
| `scripts/validate.py` | Validation du schéma et des références aux partis |
| `.claude/skills/watch-candidates/` | Procédure de veille des nouvelles candidatures |

## Conventions

- Clés en anglais, valeurs en français, dates au format ISO (`AAAA-MM-JJ`).
- L'âge n'est pas stocké : il se calcule à partir de `birth_date`.
- `null` signifie « non vérifié », pas « inexistant ». Les champs à confirmer
  sont listés dans `verification.to_verify` de chaque fiche.
- Statuts de candidature : `declared`, `invested` (désignation par un parti ou
  une primaire), `sponsorships_validated` (liste officielle du Conseil
  constitutionnel), `withdrawn`.

## Validation

```sh
pip install pyyaml jsonschema
python scripts/validate.py
```

## Avertissement

La liste officielle n'existera qu'après validation des 500 parrainages par le
Conseil constitutionnel, au printemps 2027. D'ici là, ces données reflètent les
annonces relayées par la presse, avec leurs sources.
