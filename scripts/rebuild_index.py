"""
MediConnect HMS — Build & Sync Script
Compiles src/ components into appBundle.jsx and updates frontend/index.html and root index.html.
"""

import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_BUNDLE = os.path.join(ROOT_DIR, 'src', 'appBundle.jsx')
FRONTEND_INDEX = os.path.join(ROOT_DIR, 'frontend', 'index.html')
ROOT_INDEX = os.path.join(ROOT_DIR, 'index.html')

if not os.path.exists(SRC_BUNDLE):
    print(f"ERROR: {SRC_BUNDLE} not found. Run build_bundle.py first.")
    exit(1)

with open(SRC_BUNDLE, 'r', encoding='utf-8') as f:
    bundle_code = f.read()

pattern = re.compile(r'<script\s+type="text/babel"[^>]*>', re.IGNORECASE)

for target_file in [FRONTEND_INDEX, ROOT_INDEX]:
    if not os.path.exists(target_file):
        continue

    with open(target_file, 'r', encoding='utf-8') as f:
        html = f.read()

    match = pattern.search(html)
    if not match:
        print(f'ERROR: Could not find <script type="text/babel"> in {target_file}')
        continue

    start_tag_end = match.end()
    end_idx = html.find('</script>', start_tag_end)
    if end_idx == -1:
        print(f'ERROR: Could not find closing </script> in {target_file}')
        continue

    new_html = html[:start_tag_end] + '\n' + bundle_code + '\n' + html[end_idx:]

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f'{os.path.basename(target_file)} updated! Size: {len(new_html) // 1024} KB')
