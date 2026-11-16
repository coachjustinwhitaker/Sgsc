# Coach tool (prototype)

Brand-free records in, pages out.

- `data/activities/`: one file per activity. The library.
- `data/plans/`: one file per age and track. Weeks refer to activities by id.
- `data/blocks.yaml`: block names and group headings.
- `rules/ladder.yaml`: which blocks and levels each age and track uses.
- `theme/<brand>/`: name, logo and wording for one brand. Nothing else mentions a brand.
- `templates/`: page shells with `{{tokens}}`.
- `tools/check.py`: validates the records. `tools/build.py <plan> <brand>`: writes `build/<plan>.<brand>.html`.
- `tools/import_u10.py`: one-time import from the old U10 page, kept for provenance.

Run: `python3 tools/check.py` then `python3 tools/build.py u10-rec sgsc`.

## Adding activities and diagrams
- Easiest: open `build/activity-builder.html` (made by `python3 tools/build.py author`), add activities or load one to edit, download the batch, then run `python3 tools/import_csv.py activity-batch.json`.
- Or fill in `data/templates/activities-template.csv` (one row per activity; lists use semicolons), then run `python3 tools/import_csv.py yourfile.csv`. It checks everything and keeps nothing if a row fails. Add `--update` to overwrite existing ids.
- Diagrams: export a PNG, JPG, WebP or SVG, put it in `data/diagrams/`, and put the file name in the `diagram` column (or the `diagram:` field of the record). Keep them brand-free. The app embeds them at up to 720px wide.

## Core and club layers
Core records (`data/`) are brand-free. Club-specific content lives in `theme/<club>/`: `brand.yaml` for names, colors and logo, and `overlay/<age>.yaml` for things like game format, pathway text and contacts. Test: would another club change it? Yes means overlay. Delete the overlay folder and the app shows core content only.
