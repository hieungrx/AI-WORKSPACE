#!/usr/bin/env python3
"""Minimal, offline, dependency-free integrity check (not an LLM fact checker)."""
from pathlib import Path
import csv, re, sys

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / 'wiki'
MANIFEST = ROOT / 'sources' / 'manifest.csv'
problems = []

with MANIFEST.open(encoding='utf-8-sig', newline='') as fp:
    ids = {r['source_id'].strip() for r in csv.DictReader(fp) if r.get('source_id','').strip()}

link_rx = re.compile(r'(?<!!)\[[^]]+\]\(([^)]+)\)')
source_rx = re.compile(r'\bSRC-\d{8}-\d{3}\b')
for page in WIKI.rglob('*.md'):
    content = page.read_text(encoding='utf-8')
    for target in link_rx.findall(content):
        target = target.split('#',1)[0].strip()
        if not target or target.startswith(('http://','https://','mailto:')):
            continue
        resolved = (page.parent / target).resolve()
        if not resolved.exists():
            problems.append(f'BROKEN LINK {page.relative_to(ROOT)} -> {target}')
    for sid in set(source_rx.findall(content)):
        if sid not in ids:
            problems.append(f'UNKNOWN SOURCE {page.relative_to(ROOT)} -> {sid}')
    if page.name not in ('index.md','log.md') and '- **Status:**' not in content:
        problems.append(f'MISSING STATUS {page.relative_to(ROOT)}')

if problems:
    print('Workspace checks found', len(problems), 'issue(s):')
    for item in problems: print(' -', item)
    sys.exit(1)
print('PASS: local link and reference checks; NOT a factual verification.')
