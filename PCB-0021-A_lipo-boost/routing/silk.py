import pcbnew,sys,json
P=sys.argv[1];b=pcbnew.LoadBoard(P)
d=json.load(open('/tmp/c/g.json'))
loser={('J4','R6'):'R6',('D3','R7'):'R7',('L1','R8'):'R8',('L1','R5'):'R5',('C3','R8'):'R8',('C2','R9'):'R9',('C10','C14'):'C14',('C1','R4'):'R4'}
kill=set()
for f in d['failing']:
    L=loser.get(tuple(sorted(f['refs'])))
    for i in f['items']:
        if L and i['msg'].endswith('of %s on F.Silkscreen'%L): kill.add(i['uuid'])
n=0
for fp in b.GetFootprints():
    for g in list(fp.GraphicalItems()):
        if g.m_Uuid.AsString() in kill: fp.Delete(g); n+=1
l1=b.FindFootprintByReference('L1'); r=l1.Reference(); p=l1.GetPosition()
r.SetPosition(pcbnew.VECTOR2I(p.x, p.y-int(2.6e6)))
print('deleted',n,'of',len(kill)); print(pcbnew.SaveBoard(P,b))
