import pcbnew,sys
P=sys.argv[1]
b=pcbnew.LoadBoard(P)
iu=lambda v:int(round(v*1e6))
def net(n): return b.FindNet(n)
# 1 strip
rm=[]
for t in b.GetTracks():
    n=t.GetNetname()
    if n in('/CHG','/PGOOD','/EN','/DONE_A'): rm.append(t)
    elif n=='GND' and t.GetClass()=='PCB_TRACK' and t.GetWidth()<iu(0.5): rm.append(t)
for t in rm: b.Remove(t)
print('removed',len(rm))
# 2 move L1
l1=b.FindFootprintByReference('L1'); l1.Move(pcbnew.VECTOR2I(iu(0.6),0))
PR=[40]
def zone(n,layer,rects,minw=0.2,prio=None):
    for r in rects:
        PR[0]+=1
        z=pcbnew.ZONE(b);z.SetLayer(b.GetLayerID(layer));z.SetNet(net(n));z.SetAssignedPriority(PR[0])
        z.SetMinThickness(iu(minw));z.SetLocalClearance(iu(0.2));z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
        x1,y1,x2,y2=r;o=z.Outline();o.NewOutline()
        for x,y in((x1,y1),(x2,y1),(x2,y2),(x1,y2)):o.Append(iu(x),iu(y))
        b.Add(z)
def trk(n,w,pts,layer="F.Cu"):
    for a,c in zip(pts,pts[1:]):
        t=pcbnew.PCB_TRACK(b);t.SetStart(pcbnew.VECTOR2I(iu(a[0]),iu(a[1])));t.SetEnd(pcbnew.VECTOR2I(iu(c[0]),iu(c[1])))
        t.SetWidth(iu(w));t.SetLayer(b.GetLayerID(layer));t.SetNet(net(n));b.Add(t)
def via(n,x,y):
    v=pcbnew.PCB_VIA(b);v.SetPosition(pcbnew.VECTOR2I(iu(x),iu(y)));v.SetWidth(iu(0.6));v.SetDrill(iu(0.3))
    v.SetViaType(pcbnew.VIATYPE_THROUGH);v.SetNet(net(n));b.Add(v)
zone("+SYS","F.Cu",[(42.5,51.85,44.6,52.1),(44.3,48.5,45.3,49.3),(44.3,46.5,45.1,49.0)])
zone("+5V","F.Cu",[(50.5,42.9,51.3,43.6)])
zone("GND","F.Cu",[(42.0,51.33,42.6,51.61),(42.0,50.33,42.6,50.61),(41.86,51.9,42.14,52.5)])
# CHG
W=0.2
trk("/CHG",W,[(42.0,49.65),(43.0,49.65)])
via("/CHG",43.0,49.65)
trk("/CHG",W,[(43.0,49.65),(43.0,53.9),(45.3,56.2),(45.3,58.0),(49.7,62.4),(54.11,62.4),(54.11,59.4)],"B.Cu")
via("/CHG",45.3,56.2);trk("/CHG",W,[(45.3,56.2),(45.3,55.3)])
via("/CHG",54.11,61.35);trk("/CHG",W,[(54.11,61.35),(53.05,61.35)])
via("/CHG",54.11,59.4);trk("/CHG",W,[(54.11,59.4),(54.11,58.4)])
# PGOOD
trk("/PGOOD",W,[(42.75,50.97),(43.75,50.97)]);via("/PGOOD",43.75,50.97)
trk("/PGOOD",W,[(43.75,50.97),(50.9,50.97),(50.9,58.95),(51.4,59.45)],"B.Cu")
via("/PGOOD",51.4,59.45);trk("/PGOOD",W,[(51.4,59.45),(52.05,59.45)])
# EN
trk("/EN",W,[(46.2,43.85),(46.2,44.0),(49.25,44.0)])
trk("/EN",W,[(47.5,44.0),(47.5,44.4)]);via("/EN",47.5,44.4)
trk("/EN",W,[(47.5,44.4),(55.5,36.4),(62.28,36.4),(62.28,34.1)],"B.Cu")
# DONE_A
trk("/DONE_A",W,[(48.25,58.35),(48.25,64.3),(65.91,64.3),(65.91,63.17)])
for z in b.Zones():
    if z.GetNetname()=='GND' and z.IsOnLayer(0): z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
f=pcbnew.ZONE_FILLER(b);f.Fill(b.Zones())
b.Save(P);print('ok')
