from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,os
D=Path(__file__).parent/'dist'; errors=[]
c=json.loads((D.parent/'config.json').read_text());base=os.environ.get('SITE_BASE_PATH','').rstrip('/')
class Parse(HTMLParser):
 def __init__(self): super().__init__();self.links=[];self.ids=set();self.h1=0;self.title=False;self.description=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.description=True
  if 'id' in a:self.ids.add(a['id'])
  if tag in ('a','link','script','img'):
   v=a.get('href',a.get('src',''))
   if v.startswith('/') or v.startswith('#'):self.links.append(v)
  if tag=='img' and 'alt' not in a:errors.append('Missing image alt')
files=list(D.rglob('*.html'));parsed={}
for f in files:
 p=Parse();p.feed(f.read_text());parsed[f]=p
 if p.h1!=1 or not p.title or not p.description:errors.append(str(f)+' headings/metadata')
for f,p in parsed.items():
 for l in p.links:
  u=urlsplit(l); local=u.path
  if base and local.startswith(base+'/'):local=local[len(base):]
  target=D/local.lstrip('/') if local else f
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(str(f)+' missing '+l)
  elif u.fragment and target in parsed and u.fragment not in parsed[target].ids:errors.append(str(f)+' missing fragment '+l)
c=json.loads((D.parent/'config.json').read_text())
for k,v in c['simplePractice'].items():
 if v and (urlsplit(v).scheme!='https' or not urlsplit(v).netloc):errors.append('Invalid secure URL: '+k)
assert not errors,'\n'.join(errors)
print(f'PASS: {len(files)} pages; local links, anchors, image alt, headings, metadata, booking configuration')
