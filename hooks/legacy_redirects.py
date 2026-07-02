"""Emit redirect stubs for the URLs the old Jekyll site served.

Jekyll published every page as a flat file under /docs/ (e.g.
/docs/Factfulness.html). MkDocs uses directory URLs with slugged paths, so
plain mkdocs-redirects can't reproduce the old `.html` paths exactly. This
hook writes a tiny meta-refresh stub at each legacy path after the build.
"""

import os

REDIRECTS = {
    "docs/index.html": "/books/",
    "docs/Interests.html": "/interests/",
    "docs/mcp.html": "/interests/mcp/",
    "docs/rag.html": "/interests/rag/",
    "docs/Business Model Generation.html": "/books/business-model-generation/",
    "docs/Escape Velocity.html": "/books/escape-velocity/",
    "docs/Factfulness.html": "/books/factfulness/",
    "docs/Fearless.html": "/books/fearless/",
    "docs/Influence.html": "/books/influence/",
    "docs/Leaders Eat Last.html": "/books/leaders-eat-last/",
    "docs/Scrum.html": "/books/scrum/",
    "docs/Shape Up.html": "/books/shape-up/",
    "docs/Storytelling with Data.html": "/books/storytelling-with-data/",
    "docs/The Dichotomy of Leadership.html": "/books/the-dichotomy-of-leadership/",
    "docs/The First 90 Days.html": "/books/the-first-90-days/",
    "docs/The Psychology of Money.html": "/books/the-psychology-of-money/",
    "docs/Traction.html": "/books/traction/",
    "docs/Zero to One.html": "/books/zero-to-one/",
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="https://collapsed.space{url}">
<title>Redirecting…</title>
</head>
<body>
<p>This page has moved to <a href="{url}">{url}</a>.</p>
</body>
</html>
"""


def on_post_build(config, **kwargs):
    site_dir = config["site_dir"]
    for old_path, new_url in REDIRECTS.items():
        target = os.path.join(site_dir, old_path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(TEMPLATE.format(url=new_url))
