#!/usr/bin/env python3
"""Assemble portfolio pages: header + body + footer into self-contained HTML files."""
import pathlib

SRC = pathlib.Path(__file__).parent
DIST = SRC.parent / "dist"
DIST.mkdir(exist_ok=True)

PAGES = {
    "home": "Home — Asad Bukhari | WordPress Developer & AI Automation Specialist",
    "about": "About — Asad Bukhari",
    "services": "Services — Asad Bukhari",
    "projects": "Projects — Asad Bukhari",
    "skills": "Skills — Asad Bukhari",
    "contact": "Contact — Asad Bukhari",
}

css = (SRC / "style.css").read_text()
header = (SRC / "header.html").read_text()
footer = (SRC / "footer.html").read_text()

for slug, title in PAGES.items():
    body = (SRC / f"{slug}-body.html").read_text()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="Asad Bukhari — WordPress Developer & AI Automation Specialist in Lahore, Pakistan. Modern websites, AI automation, SEO and digital marketing for businesses.">
<style>{css}</style>
</head>
<body>
{header.replace('%%PAGE%%', slug)}
<main>{body}</main>
{footer.replace('%%PAGE%%', slug)}
</body>
</html>"""
    (DIST / f"{slug}.html").write_text(html)
    print("built", slug, len(html), "bytes")
