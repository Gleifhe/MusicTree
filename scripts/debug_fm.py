import re, yaml
from pathlib import Path

def read_fm(path):
    text = path.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return None, 'no frontmatter'
    try:
        d = yaml.safe_load(m.group(1)) or {}
        return d, None
    except Exception as e:
        return None, str(e)

for section in ['artists', 'people', 'albums', 'songs']:
    missing = []
    for f in sorted(Path('content/' + section).glob('*.md')):
        fm, err = read_fm(f)
        if err or not fm or not fm.get('title'):
            reason = err if err else 'no title'
            missing.append(f.stem + ': ' + reason)
    if missing:
        print('--- ' + section + ' issues ---')
        for item in missing:
            print('  ' + item)
    else:
        print(section + ': all OK (' + str(len(list(Path('content/' + section).glob('*.md')))) + ' files)')
