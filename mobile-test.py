#!/usr/bin/env python3
"""Render dist pages at mobile width, screenshot + detect horizontal overflow."""
from playwright.sync_api import sync_playwright
import pathlib, json

DIST = pathlib.Path("/home/hatch/workspace/portfolio/dist")
OUT = pathlib.Path("/home/hatch/workspace/portfolio/review-mobile")
OUT.mkdir(exist_ok=True)

DETECT = """() => {
  const vw = document.documentElement.clientWidth;
  const bad = [];
  const seen = new Set();
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 || r.left < -1) {
      let d = el.tagName.toLowerCase();
      if (el.className && typeof el.className === 'string')
        d += '.' + el.className.trim().split(/\\s+/).slice(0,3).join('.');
      const key = d + '|' + Math.round(r.width);
      if (!seen.has(key)) {
        seen.add(key);
        bad.push({el: d, left: Math.round(r.left), right: Math.round(r.right),
                  width: Math.round(r.width), text: (el.innerText||'').slice(0,60)});
      }
    }
  });
  return {vw, scrollW: document.documentElement.scrollWidth, bad: bad.slice(0, 25)};
}"""

report = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/meta-chromium/chrome",
                          args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    for slug in ["home", "about", "services", "projects", "skills", "contact"]:
        f = DIST / f"{slug}.html"
        pg.goto(f.as_uri())
        pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / f"{slug}.png"), full_page=True)
        report[slug] = pg.evaluate(DETECT)
        print(slug, "vw:", report[slug]["vw"], "scrollW:", report[slug]["scrollW"],
              "overflowers:", len(report[slug]["bad"]))
    b.close()

(OUT / "report.json").write_text(json.dumps(report, indent=1))
print("saved to", OUT)
