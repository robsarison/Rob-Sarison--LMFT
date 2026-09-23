"""Owner facts and truthful metadata; all empty settings remain unpublished."""
import html,json,re
E=html.escape
SERVICES=[('/psychotherapy/','Psychotherapy'),('/aging-memory-caregiving/','Aging, dementia & caregiving'),('/drama-therapy/','Drama therapy'),('/training-consultation/','Training & consultation')]
META={
'/':('California Therapist & Counseling | Rob Sarison, LMFT','Psychotherapy and counseling for individuals, couples and families with Robert Sarison, LMFT. San Francisco Bay Area connection and California telehealth.'),
'/about/':('About Rob Sarison, LMFT | California Psychotherapist','Meet Rob Sarison, LMFT, RDT, a California psychotherapist bringing a practical, creative approach to relationships, life transitions, aging and caregiving.'),
'/psychotherapy/':('Bay Area Psychotherapy & California Telehealth | Rob Sarison','Explore individual, couples and family psychotherapy with Rob Sarison, LMFT. Practical support for relationships and life changes through California telehealth.'),
'/psychotherapy/individual/':('Individual Therapy in California | Rob Sarison, LMFT','Individual therapy for anxiety, low mood, grief and life transitions. Explore patterns and practical next steps with Rob Sarison through California telehealth.'),
'/psychotherapy/couples/':('Couples Therapy & California Telehealth | Rob Sarison','Couples therapy with Rob Sarison, LMFT, for communication, conflict and changing expectations. Explore a more connected relationship through California telehealth.'),
'/psychotherapy/family/':('Family Therapy in California | Rob Sarison, LMFT','Family therapy for changing roles, conflict and caregiving decisions. Rob Sarison offers a practical, relational approach with California telehealth available.'),
'/psychotherapy/approach/':('A Practical Approach to Therapy | Rob Sarison, LMFT','Explore Rob Sarison’s collaborative therapy approach: relational work, CBT and DBT-informed skills, and creative techniques tailored to your goals in California.'),
'/psychotherapy/cbt-dbt/':('CBT & DBT-Informed Therapy in California | Rob Sarison','Learn how Rob Sarison integrates CBT and DBT-informed skills for emotions, coping and communication into individualized psychotherapy in California.'),
'/aging-memory-caregiving/':('Dementia & Caregiver Support in California | Rob Sarison','Support for aging, memory loss and family caregiving with Rob Sarison. Psychotherapy and dementia caregiver consultation informed by experience in aging services.'),
'/drama-therapy/':('Drama Therapy in California | Rob Sarison, LMFT, RDT','Explore drama therapy with Rob Sarison, RDT: role work, storytelling and creative ways to practice new responses. California telehealth; no acting experience needed.'),
'/training-consultation/':('Dementia Care Training & Consultation | Rob Sarison','Professional training and consultation with Rob Sarison on dementia care, caregiving, communication and drama therapy. Discuss your group’s needs and format.'),
'/fees-faq/':('Therapy Fees & California Telehealth FAQ | Rob Sarison','Understand private-pay therapy, out-of-network questions and California telehealth with Rob Sarison. Discuss session fees and arrangements before beginning care.'),
'/contact/':('Email About a Consultation | Rob Sarison, LMFT','Email Rob Sarison to arrange an initial consultation. Ask about individual, couples or family therapy, caregiving support and California telehealth.'),
'/client-portal/':('Contact & Scheduling | Rob Sarison','Contact Rob Sarison directly by email or phone to arrange appointments.'),
'/privacy/':('Website Privacy & Practice Information | Rob Sarison','Read how Rob Sarison’s website handles hosting data, email and phone contact and optional YouTube videos. No clinical forms, advertising trackers or analytics.'),
'/404.html':('Page Not Found | Rob Sarison Psychotherapy','Find your way back to Rob Sarison’s psychotherapy website, explore services, or email to arrange an initial consultation.')}

def phone_link(c):
 phone=c.get('phone')
 return '<a aria-label="Call Rob Sarison at '+E(phone)+'" href="tel:'+re.sub(r'[^+0-9]','',phone)+'">'+E(phone)+'</a>' if phone else ''

def location(c):
 text='<p><strong>California telehealth.</strong> You must be physically in California at the time of a telehealth session.</p>'
 o=c['inPerson']
 if o['offered'] is True:
  text+='<p>In-person sessions are offered'+(' in '+E(o['location']) if o.get('location') else '')+'. Discuss current availability during your consultation.</p>'
 elif o['offered'] is False:text+='<p>Sessions are offered through telehealth; in-person sessions are not available.</p>'
 else:text+='<p>Ask during your consultation about current in-person options.</p>'
 return text

def money(v):return 'No charge' if v==0 else '$'+format(v,',.2f').rstrip('0').rstrip('.')

def fact_rows(c):
 rows=[]
 for key,label in [('individual','Individual'),('couples','Couples'),('family','Family')]:
  fee=c['fees'].get(key);minutes=c['sessionLengths'].get(key)
  if fee is not None or minutes is not None:rows.append((label+' session',' · '.join(([money(fee)] if fee is not None else [])+([str(minutes)+' minutes'] if minutes is not None else []))))
 con=c['consultation']
 if con['fee'] is not None or con['minutes'] is not None:rows.append(('Initial consultation',' · '.join(([money(con['fee'])] if con['fee'] is not None else [])+([str(con['minutes'])+' minutes'] if con['minutes'] is not None else []))))
 if c['paymentMethods']:rows.append(('Payment methods',', '.join(c['paymentMethods'])))
 if c['superbillsOffered'] is not None:rows.append(('Superbills','Available on request; reimbursement depends on your plan.' if c['superbillsOffered'] else 'Not offered.'))
 cancel=c['cancellation']
 if cancel['windowHours'] is not None:rows.append(('Cancellation notice',str(cancel['windowHours'])+' hours'))
 if cancel['fee'] is not None:rows.append(('Cancellation fee',money(cancel['fee'])))
 return '<dl class="practice-facts">'+''.join('<div><dt>'+E(a)+'</dt><dd>'+E(b)+'</dd></div>' for a,b in rows)+'</dl>' if rows else ''

def refine(path,body,c,button):
 if path=='/about/':
  license='<br>California LMFT license '+E(str(c['licenseNumber'])) if c.get('licenseNumber') else ''
  body=body.replace('Licensed Marriage and Family Therapist (LMFT)<br>Registered Drama Therapist (RDT)', 'Licensed Marriage and Family Therapist (LMFT)'+license+'<br>Registered Drama Therapist (RDT)')
  body=body.replace('<h2>Professional credentials</h2>', '<h2>Credentials & approach</h2>')
  body=body.replace('<p><a href="/psychotherapy/approach/">Explore', '<p><strong>Who I help:</strong> individuals, couples, families, and people navigating aging and caregiving.</p><p><strong>Approaches:</strong> relational and family systems psychotherapy, CBT and DBT-informed strategies, and drama therapy.</p><p><strong>Relevant experience:</strong> psychotherapy, dementia-care leadership, professional training, and consultation.</p><p><a href="/psychotherapy/approach/">Explore')
 if path=='/fees-faq/':
  body='<div class="wrap"><section class="pagehero"><p class="eyebrow">Fees & frequently asked questions</p><h1>Clear information.<br>A thoughtful beginning.</h1><p class="lead">Understand the practical arrangements before you begin.</p></section><div class="article"><h2>Private pay. Informed choices.</h2><p>This is a private-pay practice. If your plan offers out-of-network benefits, ask your insurer about eligibility, deductibles, reimbursement and required documentation. Reimbursement is not guaranteed.</p>'+fact_rows(c)+'<p>We’ll discuss session fees, length, payment arrangements and cancellation terms before starting. Ask during your consultation about any details you need.</p><h2>Where we meet</h2>'+location(c)+'<p>Virtual sessions are conducted through the SimplePractice telehealth platform. Contact me by email or phone to arrange a consultation or appointment.</p><h2>Common questions</h2>'
  questions=[('What are your professional credentials?','Robert Sarison is a California Licensed Marriage and Family Therapist (LMFT), License #38316, and a Registered Drama Therapist (RDT). He is also a Dementia Capable Care Specialist (DCCS).'),('How do I begin?','Email <a href="mailto:robsarison@gmail.com">robsarison@gmail.com</a> or call <a href="tel:4156131946">415.613.1946</a>. We’ll discuss your needs and arrange a consultation directly. There is no online booking calendar.'),('Can I use insurance?','You pay the practice directly. Out-of-network reimbursement is determined by your insurer. '+('Superbills are available on request.' if c['superbillsOffered'] is True else 'Ask during your consultation about documentation.' if c['superbillsOffered'] is None else 'The practice does not offer superbills.')),('How long will therapy take?','The pace and length of therapy depend on your goals and circumstances. We’ll review progress together; there is no guaranteed outcome or fixed timetable.'),('Does a request make me a client?','No. Submitting a request does not establish a therapist-client relationship. Services begin only after we agree to proceed and complete intake and consent arrangements.')]
  body+=''.join('<details class="faq"><summary>'+q+'</summary><p>'+a+'</p></details>' for q,a in questions)+'</div></div>'
 return body

def schema(c,path,title):
 root=c['origin'].rstrip('/');person=root+'/#rob';practice=root+'/#practice'
 p={'@type':'Person','@id':person,'name':c['name'],'honorificSuffix':c['credentials'],'jobTitle':'Licensed Marriage and Family Therapist','url':root+'/','image':root+'/rob-portrait-1200.webp','hasCredential':[{'@type':'EducationalOccupationalCredential','name':'Licensed Marriage and Family Therapist (LMFT)'},{'@type':'EducationalOccupationalCredential','name':'Registered Drama Therapist (RDT)'}]}
 if c.get('licenseNumber'):p['identifier']='California LMFT '+str(c['licenseNumber'])
 if c.get('socialLinks'):p['sameAs']=c['socialLinks']
 service={'@type':'ProfessionalService','@id':practice,'name':c['name']+' Psychotherapy','url':root+'/','image':root+'/social-preview.png','founder':{'@id':person},'areaServed':[{'@type':'State','name':'California'},{'@type':'Place','name':c['location']}],'hasOfferCatalog':{'@type':'OfferCatalog','name':'Practice services','itemListElement':[{'@type':'Offer','itemOffered':{'@type':'Service','name':name,'url':root+route,'provider':{'@id':person}}} for route,name in SERVICES]}}
 if c.get('phone'):service['telephone']=c['phone']
 if c.get('officeAddress'):service['address']={'@type':'PostalAddress','streetAddress':c['officeAddress']}
 nodes=[p,service,{'@type':'WebSite','@id':root+'/#website','name':c['name']+' Psychotherapy','url':root+'/','publisher':{'@id':practice}}]
 if path!='/':nodes.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':root+'/'},{'@type':'ListItem','position':2,'name':title.split(' | ')[0],'item':root+path}]})
 return {'@context':'https://schema.org','@graph':nodes}
