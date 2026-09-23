"""Validate generated pages, owner facts, privacy boundaries and deployment paths."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,os,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).parent
S=ROOT/'site' if (ROOT/'site/config.json').exists() else ROOT
c=json.loads((S/'config.json').read_text())
D=Path(os.environ.get('SITE_OUTPUT',str(ROOT/'dist')))
origin=os.environ.get('SITE_ORIGIN',c['origin']).rstrip('/')
base=os.environ.get('SITE_BASE_PATH',urlsplit(origin).path).rstrip('/')
errors=[]
class Parse(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.ids=set();self.h1=0;self.titles=[];self.metas={};self.canon=[];self.jsons=[];self.capture=None;self.buf='';self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='title':self.capture='title';self.buf=''
  if tag=='script' and a.get('type')=='application/ld+json':self.capture='json';self.buf=''
  if tag=='meta':
   key=a.get('name',a.get('property'));self.metas.setdefault(key,[]).append(a.get('content',''))
  if tag=='link' and a.get('rel')=='canonical':self.canon.append(a.get('href'))
  if 'id' in a:
   if a['id'] in self.ids:errors.append('Duplicate ID: '+a['id'])
   self.ids.add(a['id'])
  for key in ['href','src','action','poster']:
   v=a.get(key,'')
   if v.startswith('http:') or v.startswith('//'):errors.append('Insecure resource: '+v)
   if v.startswith('mailto:') and v.split('?',1)[0]!='mailto:'+str(c.get('email')):errors.append('Unapproved email address')
   if 'clientsecure.me' in v:errors.append('Unexpected scheduling platform link')
   if v.startswith('/') or v.startswith('#'):self.links.append(v)
  if tag in ('form','input','textarea'):errors.append('Unexpected form/input collection')
  if tag=='img':
   if 'alt' not in a:errors.append('Missing image alt')
   if not a.get('width') or not a.get('height'):errors.append('Missing image dimensions')
   for entry in a.get('srcset','').split(','):
    if entry.strip():self.links.append(entry.strip().split()[0])
 def handle_endtag(self,tag):
  if tag=='title' and self.capture=='title':self.titles.append(self.buf);self.capture=None
  if tag=='script' and self.capture=='json':
   try:self.jsons.append(json.loads(self.buf))
   except ValueError:errors.append('Malformed JSON-LD')
   self.capture=None
 def handle_data(self,data):
  if self.capture:self.buf+=data
  else:self.text.append(data)
files=sorted(D.rglob('*.html'));parsed={};titles=set();descriptions=set();canonicals=set()
for f in files:
 p=Parse();p.feed(f.read_text());parsed[f]=p
 def fail(message):errors.append(str(f.relative_to(D))+': '+message)
 if p.h1!=1:fail('Expected one H1')
 if len(p.titles)!=1 or not p.titles[0].strip():fail('Missing/duplicate title')
 elif p.titles[0] in titles:fail('Non-unique title')
 else:titles.add(p.titles[0])
 desc=p.metas.get('description',[])
 if len(desc)!=1 or not desc[0]:fail('Missing/duplicate description')
 elif desc[0] in descriptions:fail('Non-unique description')
 else:descriptions.add(desc[0])
 rel=f.relative_to(D).as_posix();route='/' if rel=='index.html' else '/'+rel.removesuffix('index.html')
 expected=origin+route
 if p.canon!=[expected]:fail('Canonical mismatch '+str(p.canon))
 if p.metas.get('og:url')!=[expected]:fail('Missing/mismatched OG URL')
 for key in ['og:title','og:description','og:image','twitter:image']:
  if len(p.metas.get(key,[]))!=1:fail('Missing/duplicate '+key)
 if p.metas.get('og:image')!=[origin+'/social-preview.png']:fail('OG image origin mismatch')
 if p.metas.get('twitter:card')!=['summary_large_image']:fail('Social card mismatch')
 if not p.jsons or not all(x.get('@context')=='https://schema.org' and x.get('@graph') for x in p.jsons):fail('Missing structured-data graph')
 if f.name!='404.html':canonicals.add(expected)
 if c['publicLaunch'] and re.search(r'fictional|staging examples|\$___|not yet published|sample quote',' '.join(p.text),re.I):fail('Public placeholder/sample content')
for f,p in parsed.items():
 for link in p.links:
  u=urlsplit(link);local=unquote(u.path)
  if base and local:
   if not local.startswith(base+'/'):errors.append('Wrong base path '+link);continue
   local=local[len(base):]
  target=D/local.lstrip('/') if local else f
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(str(f)+' missing '+link)
  elif u.fragment and target in parsed and u.fragment not in parsed[target].ids:errors.append(str(f)+' missing fragment '+link)
for key,value in c['simplePractice'].items():
 if value and (urlsplit(value).scheme!='https' or not urlsplit(value).netloc):errors.append('Invalid secure URL: '+key)
if c['publicLaunch'] and c.get('testimonials'):errors.append('Unreviewed testimonial config is not allowed')
try:
 sitemap={e.text for e in ET.parse(D/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
 if sitemap!=canonicals:errors.append('Sitemap differs from public canonical routes')
except Exception as ex:errors.append('Invalid sitemap: '+str(ex))
if c['publicLaunch'] and 'Sitemap: '+origin+'/sitemap.xml' not in (D/'robots.txt').read_text():errors.append('Robots origin mismatch')
if urlsplit(origin).hostname==c.get('customDomain'):
 if not (D/'CNAME').exists() or (D/'CNAME').read_text()!='robsarison.com\n':errors.append('Custom-domain CNAME missing')
elif (D/'CNAME').exists():errors.append('Premature custom-domain CNAME')
assert not errors,'\n'.join(errors)
print(f'PASS: {len(files)-1} public routes + 404; metadata, schema, assets, links, paths, privacy and sitemap')
