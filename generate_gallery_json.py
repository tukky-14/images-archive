#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from typing import Dict, List

ROOT = os.path.dirname(os.path.abspath(__file__))

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg', '.PNG', '.JPG', '.JPEG', '.GIF', '.BMP', '.WEBP', '.SVG'}
PDF_EXTS = {'.pdf', '.PDF'}


def collect() -> List[Dict]:
    items: List[Dict] = []
    for base, dirs, files in os.walk(ROOT):
        # skip hidden
        if any(seg.startswith('.') for seg in os.path.relpath(base, ROOT).split(os.sep)):
            continue
        # skip assets directory itself
        rel_base = os.path.relpath(base, ROOT)
        if rel_base == '.':
            rel_base = ''
        for f in files:
            if f.startswith('.'):
                continue
            ext = os.path.splitext(f)[1]
            lower_ext = ext.lower()
            if lower_ext not in {e.lower() for e in IMAGE_EXTS | PDF_EXTS}:
                continue
            rel_path = os.path.join(rel_base, f) if rel_base else f
            if rel_path.startswith('assets' + os.sep):
                continue
            if rel_path in {'gallery.json', 'reorganize_images.py', 'generate_gallery_json.py', 'README.md', 'index.html'}:
                continue
            item_type = 'pdf' if lower_ext in {e.lower() for e in PDF_EXTS} else 'image'
            items.append({
                'path': rel_path,
                'name': f,
                'dir': rel_base.replace('\\', '/'),
                'type': item_type,
                'ext': lower_ext,
            })
    # stable sort by dir then name
    items.sort(key=lambda x: (x['dir'], x['name']))
    return items


def main() -> None:
    items = collect()
    out = {
        'generated': True,
        'count': len(items),
        'items': items,
    }
    out_path = os.path.join(ROOT, 'gallery.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(items)} items to gallery.json")


if __name__ == '__main__':
    main()


