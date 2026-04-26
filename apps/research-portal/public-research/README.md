# HIV Cure Research Radar

Static public read-only website that lists the latest 100 HIV cure-related
research records from the Europe PMC REST API, sorted by publication date.

## Run Locally

```bash
cd apps/research-portal/public-research
python3 -m http.server 4173
```

Open:

```text
http://localhost:4173
```

## Data Source

The page calls:

```text
https://www.ebi.ac.uk/europepmc/webservices/rest/search
```

The query uses Europe PMC's `sort_date:y` search modifier and `pageSize=100`.

## Boundary

This is an informational research metadata view. It does not provide medical,
clinical, or laboratory guidance.

