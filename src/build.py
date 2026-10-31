#!/usr/bin/env python3
"""Assemble portfolio pages: style + header + body + footer into WP-ready fragments.

NOTE (Oct 2026 SEO fix): output is intentionally NOT a full HTML document.
Rank Math supplies the real <title>/meta in <head>; pasting a second
<!DOCTYPE>/<html>/<head>/<title> inside a Custom HTML block created duplicate
title/meta elements in <body>. These fragments contain only <style> + content.
"""
import pathlib

SRC = pathlib.Path(__file__).parent
DIST = SRC.parent / "dist"
DIST.mkdir(exist_ok=True)

PAGES = ["home", "about", "services", "projects", "skills", "contact", "privacy"]

css = (SRC / "style.css").read_text()
header = (SRC / "header.html").read_text()
footer = (SRC / "footer.html").read_text()

for slug in PAGES:
    body = (SRC / f"{slug}-body.html").read_text()
    html = f"""<style>{css}</style>
{header.replace('%%PAGE%%', slug)}
<main>{body}</main>
{footer.replace('%%PAGE%%', slug)}"""
    (DIST / f"{slug}.html").write_text(html)
    print("built", slug, len(html), "bytes")
