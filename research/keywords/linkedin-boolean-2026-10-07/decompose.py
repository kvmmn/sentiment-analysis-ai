import itertools, json, re
A = ['architecture','architectural','architect','architects','"architectural education"','"architectural design"','"architecture students"','"building design"','"computational design"','AEC']
B = ['"artificial intelligence"','AI','GenAI','Midjourney','ChatGPT']
C = ['skills','expertise','learning','creativity','judgment','upskilling','reskilling','deskilling','augmentation','"critical thinking"','"professional identity"','"human-AI collaboration"','"role of the architect"']
def chunks(x,n): return [x[i:i+n] for i in range(0,len(x),n)]
def blk(t): return '('+' OR '.join(t)+')' if len(t)>1 else t[0]
qs=[]
for a,b,c in itertools.product(chunks(A,2),chunks(B,2),chunks(C,2)):
    q=f"{blk(a)} AND {blk(b)} AND {blk(c)}"
    ops=len(re.findall(r'\b(AND|OR|NOT)\b',q))
    assert ops<=5 and len(q)<=500,(q,ops)
    qs.append(q)
covered=set()
for a,b,c in itertools.product(chunks(A,2),chunks(B,2),chunks(C,2)):
    covered|=set(itertools.product(a,b,c))
assert covered==set(itertools.product(A,B,C)) and len(covered)==650
json.dump(qs,open('subqueries.json','w'),ensure_ascii=False,indent=0)
print(len(qs),'subqueries; triples covered',len(covered),'; max chars',max(map(len,qs)))
print(json.dumps(qs,ensure_ascii=False))
