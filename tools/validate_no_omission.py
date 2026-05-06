#!/usr/bin/env python3
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'manifests/src_manifest.json').read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024), b''):
            h.update(c)
    return h.hexdigest()
expected_modified=set(DATA.get('release_modified_files',[]))
missing=[]; mismatch=[]; preserved=0; modified=0
for item in DATA['files']:
    p=ROOT/item['packed_relpath']
    if not p.exists():
        missing.append(item['packed_relpath']); continue
    actual=sha(p)
    if actual==item['sha256']:
        preserved+=1
    elif item['packed_relpath'] in expected_modified:
        modified+=1
    else:
        mismatch.append((item['packed_relpath'], item['sha256'], actual))
if missing or mismatch:
    print('VALIDATION_FAILED')
    print('missing=', len(missing), 'mismatch=', len(mismatch))
    for x in missing[:30]: print('MISSING', x)
    for x in mismatch[:30]: print('MISMATCH', x[0], x[1], x[2])
    raise SystemExit(1)
print('VALIDATION_OK')
print(f"source_files={len(DATA['files'])}")
print(f"byte_preserved={preserved}")
print(f"release_modified={modified}")
for k,v in DATA['source_counts'].items(): print(f"{k}_files={v}")
