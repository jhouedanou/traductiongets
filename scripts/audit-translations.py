#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit i18n coverage: missing en.json keys + visible French text without data-i18n."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from bs4 import BeautifulSoup, Comment, NavigableString

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    "actualites.html", "plan-du-site.html", "mentions-legales.html",
    "index.html", "contact.html",
    "gouvernance-advisors/index.html",
    "candidats-mandataires-administratrices-administrateurs-7/index.html",
] + [str(p.relative_to(ROOT)) for p in (ROOT / "pages").glob("*.html")]

SKIP_PAGES = {"pages/0-template.html", "pages/article-template.html",
              "pages/construction-template.html", "pages/template-bootstrap.html"}

with open(ROOT / "data/translations/en.json", encoding="utf-8") as f:
    EN = json.load(f)


def resolve(key):
    cur = EN
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


# French signal: accented chars or common French stopwords as whole words
FR_WORDS = re.compile(
    r"[àâéèêëîïôûùüçœÀÂÉÈÊËÎÏÔÛÙÜÇŒ]|"
    r"\b(le|la|les|des|une|du|au|aux|et|ou|pour|avec|sur|dans|par|nous|vous|"
    r"voir|cliquer|ici|page|accueil|suivant|précédent|lire|plus|nos|vos|notre|votre|"
    r"télécharger|retour|envoyer|détails|en savoir)\b", re.IGNORECASE)

SKIP_TAGS = {"script", "style", "noscript", "template"}

missing_keys = {}
untranslated = {}

for rel in sorted(set(PAGES)):
    rel_norm = rel.replace("\\", "/")
    if rel_norm in SKIP_PAGES:
        continue
    path = ROOT / rel_norm
    if not path.exists():
        continue
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    # 1. data-i18n keys missing in en.json
    for el in soup.select("[data-i18n]"):
        key = el["data-i18n"]
        if resolve(key) is None:
            missing_keys.setdefault(rel_norm, []).append(key)
    for attr in ("placeholder", "alt", "title", "aria-label"):
        for el in soup.select(f"[data-i18n-{attr}]"):
            key = el[f"data-i18n-{attr}"]
            if resolve(key) is None:
                missing_keys.setdefault(rel_norm, []).append(f"{key} (attr:{attr})")

    # 2. visible French text not covered by any [data-i18n] ancestor
    body = soup.body
    if body is None:
        continue
    for text in body.find_all(string=True):
        if isinstance(text, Comment):
            continue
        s = str(text).strip()
        if len(s) < 3 or not FR_WORDS.search(s):
            continue
        covered = False
        node = text.parent
        while node is not None:
            if node.name in SKIP_TAGS:
                covered = True  # not visible
                break
            if getattr(node, "attrs", None) and (
                    node.has_attr("data-i18n")):
                covered = True
                break
            node = node.parent
        if not covered:
            snippet = re.sub(r"\s+", " ", s)[:90]
            untranslated.setdefault(rel_norm, []).append(snippet)

print("=== MISSING EN KEYS ===")
for page, keys in missing_keys.items():
    print(f"\n{page}:")
    for k in keys:
        print(f"  {k}")
if not missing_keys:
    print("(none)")

print("\n=== FRENCH TEXT WITHOUT data-i18n ===")
for page, snips in untranslated.items():
    print(f"\n{page}: ({len(snips)})")
    for s in snips:
        print(f"  | {s}")
if not untranslated:
    print("(none)")
