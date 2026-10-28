# Hiring-signal prospector

Turns job postings into a ranked list of companies worth contacting. A company that is hiring a
GTM engineer, with a stack your offer plugs into, is telling you what it needs this quarter.

```
python -m prospector --input sample_data/postings.json --top 10 --out ranking.csv
```

```
60 postings -> 54 companies

 62  GroTech Search     1 role(s)  Clay, HubSpot, LLM/AI, Python, SQL, Zapier, n8n
 62  Loadsmart          1 role(s)  Apollo, Clay, Gong, LLM/AI, Sales Navigator, Salesforce, ...
 62  SPS Commerce       1 role(s)  Clay, Gong, LLM/AI, Python, Salesforce, Snowflake, Zapier, ...
 62  Tekion Corp        1 role(s)  Clay, HubSpot, LLM/AI, Salesforce
 58  Google             2 role(s)  LLM/AI, Python, SQL, Salesforce
```

## What it does

1. **Extract** (`prospector/extract.py`): plain regexes pull tools (Clay, HubSpot, Salesforce, n8n,
   Apollo, Python, SQL, an LLM/AI group and more), the first "N years" ask, and an annual pay
   range from each posting. "Outreach" only counts as the product (outreach.io), not the word.
2. **Roll up** (`prospector/score.py`): postings are grouped by company.
3. **Score 0 to 100**, with the reasons printed next to every number:
   35 for number of open roles (capped at 4), 25 for hiring a GTM/growth engineer,
   30 for overlap with the tools you pass in `--target-tools`, 10 for an AI-workflow signal.

`--target-tools` is the point: set it to the tools your offer plugs into and the ranking changes.

## What the sample shows

From the 60 included postings: 33 mention LLM/AI work, 14 name Clay, 13 Salesforce, 9 HubSpot and
7 n8n. Only 6 of the 54 companies have more than one open role. Only 8 postings state a years-of-
experience ask (median 5) and 4 post a pay range, so those two fields are thin in this sample.

## Limits

- Regex extraction has false positives and misses, for example a tool named only by its category.
- The score is a hand-set heuristic, not a trained model. The weights are in `WEIGHTS`.
- Postings are a hiring signal, not a buying signal. Treat the ranking as a shortlist to research.
- `sample_data/postings.json` holds 60 public LinkedIn postings with text cut to 2,500
  characters, collected on 2026-10-28 through treg's LinkedIn jobs endpoint (about $0.02 per
  25 postings). Posting text belongs to the employers; it is included only so the repo runs.

## Tests

```
python -m unittest discover -s tests
```

Python 3.10+, standard library only.
