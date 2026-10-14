---
name: watch-candidates
description: Check for new declared candidates, withdrawals and status changes for the 2027 French presidential election, then update data/candidates.yaml, data/parties.yaml and data/watchlist.yaml. Use when asked to "surveiller les candidats", "mettre à jour la liste des candidats", "nouveaux candidats ?", or when a scheduled routine runs this skill.
---

# Watch candidates

Keep `data/candidates.yaml` in line with the news. Only explicitly declared
candidates go in that file. Everyone else stays in `data/watchlist.yaml`.

## Steps

1. Read `data/candidates.yaml`, `data/parties.yaml` and `data/watchlist.yaml`.
   Note `meta.last_updated`: search only for what changed since that date.

2. Search the news (French queries work best), for example:
   - `présidentielle 2027 annonce candidature` plus the current month
   - `présidentielle 2027 retire sa candidature`
   - one query per watchlist person: `<name> candidature présidentielle 2027`
   - once the Conseil constitutionnel publishes it (spring 2027):
     `liste officielle candidats présidentielle 2027 Conseil constitutionnel`

3. For each finding, require an explicit announcement ("je suis candidat",
   official party designation, primary result) reported by a national outlet
   (LCP, Public Sénat, franceinfo, AFP relays, Le Monde, Le Figaro, Libération,
   France 24, Euronews...). Aggregator sites alone are not enough: they can
   create a watchlist entry with `status: unconfirmed`, not a candidate record.

4. Apply the change:
   - **New declaration**: add a record to `candidates.yaml` following the
     existing ones (all keys present, unknown values as `null`, field names
     listed in `verification.to_verify`). Remove the person from the watchlist.
     Add the party to `parties.yaml` if missing.
   - **Party designation or primary win**: `status: invested`, set
     `designation_date`.
   - **Withdrawal**: keep the record, set `status: withdrawn`,
     `withdrawal_date`, and say in `notes` whom they now support.
   - **Official list published**: `status: sponsorships_validated` for every
     listed candidate; withdraw the others.
   - **Filling gaps**: when a source confirms a field in `to_verify`
     (birth date, Wikidata QID, websites, program URL), fill it and drop it
     from the list. When the list is empty, set `verification.status: verified`.
   - **Campaign sites**: for every record whose `links.campaign_site_status`
     is `not_found` or `probable`, search for the site again. Upgrade to
     `confirmed` only when the press or the candidate's own declaration
     cites the address. Aggregators (elyseescope, votons-2027, repere2027...)
     and fan sites never count.
   - Always add the source URL with `accessed: <today>`.

5. Set `meta.last_updated` to today in every file you touched, then run
   `python scripts/validate.py` and fix any error.

6. Commit with a message summarising the changes (e.g.
   `data: add X (declared 2026-11-02), withdraw Y`) and push to `main`.
   If nothing changed, do not commit; just report "no change".

## Rules

- Never invent a date, URL or Wikidata QID. Use `null` and `to_verify`.
- Keys stay in English, values in French.
- Do not delete a candidate record: history matters for the promises tool.
- Report a short summary of what changed, with the sources, to the user.
