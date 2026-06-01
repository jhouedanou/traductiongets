#!/usr/bin/env python3
"""
translate_google_remaining.py — Translate only the remaining French strings
in en.json using Google Translate, preserving existing English translations.
"""

import json
import os
import re
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR_JSON = os.path.join(ROOT, "data", "translations", "fr.json")
EN_JSON = os.path.join(ROOT, "data", "translations", "en.json")

# Patterns that indicate a string still contains French text
FRENCH = re.compile(
    r"(dispose d'|d'une |d'un |au sein|à l'|Après |Depuis |Aujourd'hui|"
    r"d'expérience|s'est|qu'il|qu'elle|qu'on|notamment|grâce|également|"
    r"afin|ainsi|puis|auprès|d'administratrice|d'administrateur|"
    r"Indépendante|indépendante|expérimentée|Expérimentée|"
    r"managériale|Managériale|compétences|activités|différents|différentes|"
    r"précisant|exercé|mené|menée|rejoint|réalisé|créé|créée|"
    r"Candidat à|Candidate à|administratrice indépendante)",
    re.IGNORECASE
)


def has_french(value):
    if not isinstance(value, str):
        return False
    text = re.sub(r'<[^>]+>', ' ', value)
    text = re.sub(r'&[a-z]+;', ' ', text)
    return bool(FRENCH.search(text))


def get_nested(data, path):
    cur = data
    for k in path:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and isinstance(k, int) and k < len(cur):
            cur = cur[k]
        else:
            return None
    return cur


def set_nested(data, path, value):
    cur = data
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]] = value


def collect_french_paths(data, path=[]):
    """Walk en.json, find all string values that still look French."""
    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            results.extend(collect_french_paths(v, path + [k]))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            results.extend(collect_french_paths(v, path + [i]))
    elif isinstance(data, str):
        if has_french(data):
            results.append(tuple(path))
    return results


def google_translate_raw(text, sl='fr', tl='en'):
    url = 'https://translate.googleapis.com/translate_a/single'
    params = {'client': 'gtx', 'sl': sl, 'tl': tl, 'dt': 't', 'q': text}
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{qs}", headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        res = json.loads(r.read().decode('utf-8'))
        parts = [p[0] for p in res[0] if p[0]]
        return ''.join(parts)


def translate_single(text):
    for attempt in range(3):
        try:
            return google_translate_raw(text)
        except Exception as e:
            print(f"  [Attempt {attempt+1}] Error: {e}")
            time.sleep(1.5 * (attempt + 1))
    return text


def translate_batch(batch_items):
    """batch_items: list of (path, fr_text)"""
    html_parts = [f'<item-trans id="{i}">{text}</item-trans>'
                  for i, (_, text) in enumerate(batch_items)]
    payload = "".join(html_parts)
    try:
        translated = google_translate_raw(payload)
    except Exception as e:
        print(f"  Batch HTTP error: {e}")
        return None

    try:
        soup = BeautifulSoup(translated, 'html.parser')
        items = soup.find_all('item-trans')
        if len(items) != len(batch_items):
            print(f"  Count mismatch: expected {len(batch_items)}, got {len(items)}")
            return None
        results = []
        for item in items:
            idx = int(item.get('id'))
            inner = "".join(str(c) for c in item.contents)
            inner = re.sub(r'<\s*/\s*([a-zA-Z0-9]+)\s*>', r'</\1>', inner)
            results.append((batch_items[idx][0], inner))
        return results
    except Exception as e:
        print(f"  Batch parse error: {e}")
        return None


def main():
    print("=" * 60)
    print("Google Translate — remaining French strings only")
    print("=" * 60)

    with open(FR_JSON, encoding='utf-8') as f:
        fr_data = json.load(f)
    with open(EN_JSON, encoding='utf-8') as f:
        en_data = json.load(f)

    # Find all paths in en.json that still have French text
    french_paths = collect_french_paths(en_data)
    print(f"Found {len(french_paths)} strings still in French.")

    # Build list of (path, fr_source_text) — use fr.json as translation source
    to_translate = []
    for path in french_paths:
        fr_val = get_nested(fr_data, list(path))
        en_val = get_nested(en_data, list(path))
        if fr_val and isinstance(fr_val, str):
            to_translate.append((path, fr_val))
        elif en_val and isinstance(en_val, str):
            # No FR source found, translate the garbled EN value directly
            to_translate.append((path, en_val))

    print(f"Will translate {len(to_translate)} items (using fr.json source where available).")

    # Batch into groups of max 30 items / 2500 chars
    batches = []
    current, current_len = [], 0
    for path, text in to_translate:
        item_len = len(text) + 40
        if len(current) >= 30 or (current_len + item_len > 2500):
            batches.append(current)
            current, current_len = [], 0
        current.append((path, text))
        current_len += item_len
    if current:
        batches.append(current)

    print(f"Grouped into {len(batches)} batches.\n")

    translated = 0
    for idx, batch in enumerate(batches):
        print(f"Batch {idx+1}/{len(batches)} ({len(batch)} items)...")
        results = translate_batch(batch)
        if results:
            for path, trans in results:
                set_nested(en_data, list(path), trans)
                translated += 1
            print(f"  OK — {translated}/{len(to_translate)} done")
        else:
            print("  Batch failed, falling back to single translations...")
            for path, text in batch:
                trans = translate_single(text)
                set_nested(en_data, list(path), trans)
                translated += 1
                time.sleep(0.15)
            print(f"  Done via fallback — {translated}/{len(to_translate)}")
        time.sleep(0.4)

    # Save
    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Translated {translated} strings. Saved to {EN_JSON}")


if __name__ == "__main__":
    main()
