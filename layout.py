"""Shared editorial layouts for the interior pages; no third-party dependencies."""
import re

def polish(body):
    marker='<div class="article">'
    start=body.find(marker)
    if start<0:return body
    inner=start+len(marker);depth=1;end=None
    for match in re.finditer(r'<div\b[^>]*>|</div>',body[inner:]):
        depth+= -1 if match.group().startswith('</') else 1
        if depth==0:
            end=inner+match.start();break
    if end is None:return body
    content=body[inner:end]
    parts=re.split(r'(<h2>.*?</h2>)',content,flags=re.S)
    rows=[]
    if parts[0].strip():rows.append('<div class="editorial-intro">'+parts[0]+'</div>')
    for i in range(1,len(parts),2):
        rows.append('<section class="editorial-row"><div class="editorial-heading">'+parts[i]+'</div><div class="editorial-copy">'+parts[i+1]+'</div></section>')
    return body[:start]+'<div class="editorial">'+''.join(rows)+'</div>'+body[end+6:]
