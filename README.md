# collapsed.space

Personal notes site — book notes and interests — published at
[collapsed.space](https://collapsed.space).

Built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), deployed
to GitHub Pages by the workflow in `.github/workflows/pages.yml` on every push
to `main`.

## Local development

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Layout

- `docs/` — content (`index.md` home, `books/`, `interests/`, `assets/`)
- `mkdocs.yml` — site config, nav, theme
- `docs/assets/css/extra.css` — One Dark palette + Phosphor callout icons
- `hooks/legacy_redirects.py` — redirect stubs for the old Jekyll-era URLs

Notes are written in Obsidian; its `> [!type]` callouts are converted to
Material admonitions by the [mkdocs-callouts](https://github.com/sondregronas/mkdocs-callouts)
plugin.
