#!/usr/bin/env python3
"""
translate_google.py — Automatically translate all strings in data/translations/fr.json
to English using Google Translate free web API.
Preserves HTML formatting and handles large scale translations efficiently via batching
and robust single-item fallbacks.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

# Paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR_JSON = os.path.join(ROOT, "data", "translations", "fr.json")
EN_JSON = os.path.join(ROOT, "data", "translations", "en.json")
BACKUP_EN_JSON = os.path.join(ROOT, "data", "translations", "en.json.bak2")

MIN_TEXT_LEN = 2

def is_translatable(text):
    """Check if the text actually needs translation."""
    if not isinstance(text, str):
        return False
    txt = text.strip()
    if len(txt) < MIN_TEXT_LEN:
        return False
    if txt.isdigit():
        return False
    # Only punctuation and numbers
    if re.match(r'^[\d\s\W]+$', txt):
        return False
    # Pure URL
    if re.match(r'^https?://', txt) or re.match(r'^\.\./', txt) or re.match(r'^/[a-zA-Z0-9_-]', txt):
        return False
    # Pure Email
    if re.match(r'^[\w.+-]+@[\w-]+\.', txt):
        return False
    # Font Awesome classes/icons
    if re.match(r'^fa[srlbd]?\s+fa-', txt):
        return False
    return True

def google_translate_raw(text, sl='fr', tl='en'):
    """Make HTTP request to Google Translate free web API."""
    url = 'https://translate.googleapis.com/translate_a/single'
    params = {
        'client': 'gtx',
        'sl': sl,
        'tl': tl,
        'dt': 't',
        'q': text
    }
    query_string = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{query_string}", headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        res = json.loads(r.read().decode('utf-8'))
        parts = [p[0] for p in res[0] if p[0]]
        return ''.join(parts)

def translate_single(text, sl='fr', tl='en'):
    """Translate a single item with retries."""
    for attempt in range(3):
        try:
            return google_translate_raw(text, sl, tl)
        except Exception as e:
            print(f"  [Attempt {attempt+1}] Error translating single string: {e}")
            time.sleep(1.0 * (attempt + 1))
    return text

def translate_batch(batch_items, sl='fr', tl='en'):
    """
    Translate a batch of strings.
    batch_items: list of (path, text)
    Returns: list of (path, translated_text) or None if batch translation fails.
    """
    # Build HTML payload
    html_parts = []
    for i, (_, text) in enumerate(batch_items):
        html_parts.append(f'<item-trans id="{i}">{text}</item-trans>')
    html_payload = "".join(html_parts)

    try:
        translated_html = google_translate_raw(html_payload, sl, tl)
    except Exception as e:
        print(f"  Batch translation HTTP request failed: {e}")
        return None

    # Parse response
    try:
        soup = BeautifulSoup(translated_html, 'html.parser')
        items = soup.find_all('item-trans')
        
        # Verify count matches
        if len(items) != len(batch_items):
            print(f"  Batch count mismatch! Expected {len(batch_items)}, got {len(items)}")
            return None

        results = []
        for item in items:
            idx_str = item.get('id')
            if not idx_str:
                print("  Missing ID in translated tag")
                return None
            idx = int(idx_str)
            inner_html = "".join(str(child) for child in item.contents)
            
            # Post-process to fix any spaces in tags introduced by Google Translate
            # e.g., <span style=\"...\"> -> <span style=\"...\">
            inner_html = re.sub(r'<\s*/\s*([a-zA-Z0-9]+)\s*>', r'</\1>', inner_html)
            inner_html = re.sub(r'<\s*([a-zA-Z0-9]+)\s+([^>]+)\s*>', r'<\1 \2>', inner_html)
            
            results.append((batch_items[idx][0], inner_html))
        
        # Sort back to original order of batch_items
        return results
    except Exception as e:
        print(f"  Failed parsing translated batch: {e}")
        return None

def extract_strings(data, current_path=[]):
    """Recursively extract all translatable strings and their paths from JSON structure."""
    strings = []
    if isinstance(data, dict):
        for k, v in data.items():
            strings.extend(extract_strings(v, current_path + [k]))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            strings.extend(extract_strings(v, current_path + [i]))
    elif isinstance(data, str):
        if is_translatable(data):
            strings.append((current_path, data))
    return strings

def set_nested_value(data, path, value):
    """Set a value in a nested dict/list based on a list of keys/indices."""
    curr = data
    for i, key in enumerate(path[:-1]):
        curr = curr[key]
    curr[path[-1]] = value

def main():
    print("=" * 60)
    print("Google Translate for G&S Internationalization")
    print("=" * 60)

    # 1. Load French source JSON
    if not os.path.exists(FR_JSON):
        print(f"Error: Source file {FR_JSON} not found!")
        sys.exit(1)

    with open(FR_JSON, 'r', encoding='utf-8') as f:
        fr_data = json.load(f)

    # Make a copy for English translation
    # Non-translatable fields will naturally remain as they are in the copy
    en_data = json.loads(json.dumps(fr_data))

    # 2. Extract translatable strings
    all_items = extract_strings(fr_data)
    total_items = len(all_items)
    print(f"Found {total_items} translatable strings in fr.json.")

    # 3. Create translation batches
    # We group items such that a batch has max 40 items and max 3000 chars to avoid URL size limit
    batches = []
    current_batch = []
    current_length = 0

    for path, text in all_items:
        item_len = len(text) + 40  # estimate wrapper tag overhead
        if len(current_batch) >= 40 or (current_length + item_len > 3000):
            batches.append(current_batch)
            current_batch = []
            current_length = 0
        current_batch.append((path, text))
        current_length += item_len
    
    if current_batch:
        batches.append(current_batch)

    print(f"Grouped into {len(batches)} batches.")

    # 4. Perform translation
    translated_count = 0
    start_time = time.time()

    for idx, batch in enumerate(batches):
        print(f"\nProcessing batch {idx+1}/{len(batches)} ({len(batch)} items)...")
        
        # Try batch translation first
        batch_results = translate_batch(batch)
        
        if batch_results is not None:
            # Batch translation succeeded!
            for path, trans in batch_results:
                set_nested_value(en_data, path, trans)
                translated_count += 1
            print(f"  Batch {idx+1} succeeded. Progress: {translated_count}/{total_items}")
        else:
            # Fall back to single-item translations in case of failure
            print("  Batch failed! Falling back to item-by-item translation for this batch...")
            for path, text in batch:
                print(f"    Translating: '{text[:50]}...'")
                trans = translate_single(text)
                set_nested_value(en_data, path, trans)
                translated_count += 1
                time.sleep(0.1) # tiny sleep between fallbacks
            print(f"  Batch {idx+1} completed via fallback. Progress: {translated_count}/{total_items}")

        # Rate-limiting courtesy sleep
        time.sleep(0.3)

    # 5. Save output
    # Backup existing en.json if it exists
    if os.path.exists(EN_JSON):
        if os.path.exists(BACKUP_EN_JSON):
            os.remove(BACKUP_EN_JSON)
        os.rename(EN_JSON, BACKUP_EN_JSON)
        print(f"Backed up existing en.json to {BACKUP_EN_JSON}")

    # Write new en.json
    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print("Translation completed successfully!")
    print(f"Saved: {EN_JSON}")
    print(f"Total translated strings: {translated_count}/{total_items}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print("=" * 60)

if __name__ == "__main__":
    main()
