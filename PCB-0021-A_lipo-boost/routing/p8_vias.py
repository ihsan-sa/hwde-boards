import pcbnew,sys,math,itertools
P=sys.argv[1]
b=pcbnew.LoadBoard(P)
iu=lambda v:int(round(v*1e6))
F=b.GetLayerID("F.Cu")
gz=[z for z in b.Zones() if z.GetNetname()=="GND" and z.IsOnLayer(F)]
def inzone(x,y):
    return any(z.HitTestFilledArea(F,pcbnew.VECTOR2I(iu(x),iu(y)),0) for z in gz)
def clear(x,y):
    r=0.55
    pts=[(x,y)]+[(x+r*math.cos(a*math.pi/4),y+r*math.sin(a*math.pi/4)) for a in range(8)]
    return all(inzone(*p) for p in pts)
vias=[(t.GetX()/1e6,t.GetY()/1e6) for t in b.GetTracks() if t.GetClass()=='PCB_VIA']
def free(x,y):
    return all(math.hypot(x-vx,y-vy)>=1.0 for vx,vy in vias) and \
      all(not(p.GetPosition().x and 0) for p in [])
def padclear(x,y):
    for f in b.GetFootprints():
        for p in f.Pads():
            bb=p.GetBoundingBox(); 
            if bb.Inflate(iu(0.55)).Contains(pcbnew.VECTOR2I(iu(x),iu(y))) and p.GetNetname()!="GND": return False
    for t in b.GetTracks():
        if t.GetClass()=='PCB_TRACK' and t.GetNetname()!="GND" and t.IsOnLayer(F):
            if t.GetBoundingBox().Inflate(iu(0.6)).Contains(pcbnew.VECTOR2I(iu(x),iu(y))): return False
    return True
want={ (41.25,51.22):1,(40.0,43.75):3,(50.925,48.325):3,(48.25,55.875):0}
added=[]
for (cx,cy),n in want.items():
    cands=[]
    for dx in [i*0.2 for i in range(-14,15)]:
        for dy in [i*0.2 for i in range(-14,15)]:
            x,y=round(cx+dx,2),round(cy+dy,2)
            d=math.hypot(dx,dy)
            if d<=1.9 and clear(x,y) and padclear(x,y) and free(x,y): cands.append((d,x,y))
    cands.sort(); got=0
    for d,x,y in cands:
        if got>=n: break
        if not all(math.hypot(x-vx,y-vy)>=1.0 for vx,vy in vias): continue
        v=pcbnew.PCB_VIA(b);v.SetPosition(pcbnew.VECTOR2I(iu(x),iu(y)));v.SetWidth(iu(0.6));v.SetDrill(iu(0.3))
        v.SetViaType(pcbnew.VIATYPE_THROUGH);v.SetNet(b.FindNet("GND"));b.Add(v);vias.append((x,y));added.append((x,y));got+=1
    print((cx,cy),'want',n,'got',got,len(cands))
if len(sys.argv)>2 and sys.argv[2]=='save':
    pcbnew.SaveBoard(P,b);print('saved',added)
