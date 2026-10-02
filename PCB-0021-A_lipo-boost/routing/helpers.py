P=sys.argv[1]
b=pcbnew.LoadBoard(P)
iu=lambda v:int(round(v*1e6))
def net(n): return b.FindNet(n)
PR=[60]

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
