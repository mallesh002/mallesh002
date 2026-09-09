#!/usr/bin/env python3
"""Render public repository metadata as local SVGs. Python standard library only."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'dark': dict(bg='#0B1220', ink='#F1F6FF', muted='#A6B6CC', line='#263952', accent='#67E8F9'),
    'light': dict(bg='#F4F8FF', ink='#14233B', muted='#4D617E', line='#D1DEF0', accent='#00788C'),
}
COLORS = {'TypeScript':'#5EA3EB','JavaScript':'#E3BF52','TeX':'#83B994','Unclassified':'#8593AA','Other':'#B89CED'}


def fetch_repositories(username):
    headers = {'Accept':'application/vnd.github+json', 'User-Agent':'mallesh002-profile-snapshot', 'X-GitHub-Api-Version':'2026-03-10'}
    token=os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization']=f'Bearer {token}'
    rows=[]
    page=1
    while True:
        url=f'https://api.github.com/users/{username}/repos?type=owner&sort=full_name&per_page=100&page={page}'
        request=urllib.request.Request(url,headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            data=json.load(response)
        if not isinstance(data,list):
            raise ValueError('GitHub did not return a repository list.')
        rows.extend(data)
        if len(data)<100:
            return rows
        page+=1


def summarize(rows, username):
    if not isinstance(rows,list):
        raise ValueError('Expected an array of repository objects.')
    owned=[]
    for item in rows:
        if not isinstance(item,dict):
            raise ValueError('Invalid repository object.')
        owner=item.get('owner',{}).get('login','')
        if owner.casefold()!=username.casefold() or item.get('private') is not False:
            continue
        if 'id' not in item or 'language' not in item:
            raise ValueError('Incomplete repository metadata.')
        owned.append(item)
    # De-duplicate defensively if pagination overlaps while repositories change.
    owned=list({item['id']:item for item in owned}.values())
    languages=Counter(item['language'] or 'Unclassified' for item in owned)
    return {'username':username, 'updated_utc':datetime.now(timezone.utc).date().isoformat(),
            'public_repositories':len(owned),
            'repositories_by_primary_language':dict(sorted(languages.items(),key=lambda kv:(kv[0]=='Unclassified',-kv[1],kv[0]))),
            'scope':'Public repositories owned by this account, including forks. One primary language per repository; Unclassified means GitHub returned no primary language.',
            'source':f'https://api.github.com/users/{username}/repos'}


def txt(x,y,s,size,fill,weight=400,extra=''):
    return f'<text x="{x}" y="{y}" font-family="Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}>{escape(str(s))}</text>'


def render(data, theme, mobile=False):
    p=PALETTES[theme]
    w,h=(640,400) if mobile else (960,276)
    groups=list(data['repositories_by_primary_language'].items())
    if len(groups)>4:
        groups=groups[:3]+[('Other',sum(n for _,n in groups[3:]))]
    count=data['public_repositories']
    details=', '.join(f'{name}: {n}' for name,n in data['repositories_by_primary_language'].items()) or 'No public repositories'
    desc=f"{count} public repositories. {details}. Updated {data['updated_utc']}."
    b=f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="22" fill="{p["bg"]}" stroke="{p["line"]}"/>'
    if mobile:
        b+=txt(32,47,'PUBLIC CODE / @'+data['username'],20,p['muted'],600)
        b+=txt(32,133,count,78,p['ink'],700)
        b+=txt(138,106,'public repositories',24,p['ink'],600)
        b+=txt(32,183,'Repositories by primary language',21,p['muted'])
        bx,by,bw=32,205,576
        lx,ly,gap=32,273,290
        footer_y=365
    else:
        b+=txt(36,43,'PUBLIC CODE',17,p['muted'],600, 'letter-spacing="2"')
        b+=txt(36,134,count,84,p['ink'],700)
        b+=txt(36,172,'public repositories',22,p['ink'],600)
        b+=f'<path d="M294 36V208" stroke="{p["line"]}"/>'
        b+=txt(330,49,'Repositories by primary language',21,p['muted'])
        bx,by,bw=330,80,594
        lx,ly,gap=330,147,302
        footer_y=246
    b+=f'<defs><clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="22" rx="8"/></clipPath></defs>'
    x=bx
    b+=f'<rect x="{bx}" y="{by}" width="{bw}" height="22" rx="8" fill="{p["line"]}"/>'
    for i,(name,n) in enumerate(groups):
        color=COLORS.get(name,['#A990E4','#66BBAA','#D18AAB','#8593AA'][i%4])
        segment=bw*n/count if count else 0
        b+=f'<rect x="{x:.2f}" y="{by}" width="{segment:.2f}" height="22" fill="{color}" clip-path="url(#bar)"/>'
        x+=segment
        label_x=lx+(i%2)*gap
        label_y=ly+(i//2)*39
        b+=f'<circle cx="{label_x+5}" cy="{label_y-7}" r="5" fill="{color}"/>'
        label=name if len(name)<=15 else name[:13]+'…'
        b+=txt(label_x+20,label_y,f'{label} · {n}',21 if mobile else 19,p['ink'])
    if not groups:
        b+=txt(lx,ly,'No public repositories yet.',21,p['muted'])
    b+=txt(32 if mobile else 36,footer_y,f"Snapshot · {data['updated_utc']} UTC · Public repository metadata",16,p['muted'])
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>GitHub public repository snapshot</title><desc>{escape(desc)}</desc>{b}</svg>\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username',default='mallesh002')
    parser.add_argument('--from-repos-json',type=Path,help='Use an existing public REST repository response instead of making a request')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'assets')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?',args.username):
        parser.error('Invalid GitHub username')
    try:
        rows=json.loads(args.from_repos_json.read_text()) if args.from_repos_json else fetch_repositories(args.username)
        data=summarize(rows,args.username)
        # Render everything before writing. API or validation failures leave old assets intact.
        outputs={'github-stats.json':json.dumps(data,indent=2)+'\n'}
        for theme in PALETTES:
            for mobile in [False,True]:
                name=f'github-stats-{theme}{"-mobile" if mobile else ""}.svg'
                outputs[name]=render(data,theme,mobile)
        args.output_dir.mkdir(parents=True,exist_ok=True)
        for name,content in outputs.items():
            path=args.output_dir/name
            temporary=path.with_suffix(path.suffix+'.tmp')
            temporary.write_text(content,encoding='utf-8')
            temporary.replace(path)
    except urllib.error.HTTPError as error:
        print(f'GitHub returned HTTP {error.code}; the previous snapshot is unchanged.',file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as error:
        print(f'Snapshot update failed ({type(error).__name__}). No new snapshot should be committed.',file=sys.stderr)
        return 1
    print(f"Updated {data['username']}: {data['public_repositories']} public repositories.")
    return 0


if __name__=='__main__':
    sys.exit(main())
