import pcbnew,sys,json
b=pcbnew.LoadBoard(sys.argv[1]);m=lambda v:v/1e6
o={'pads':[],'tr':[],'via':[],'z':[]}
for f in b.GetFootprints():
    for p in f.Pads():
        bb=p.GetBoundingBox();o['pads'].append((f.GetReference()+'.'+p.GetNumber(),p.GetNetname(),m(bb.GetX()),m(bb.GetY()),m(bb.GetWidth()),m(bb.GetHeight())))
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA': o['via'].append((m(t.GetX()),m(t.GetY()),t.GetNetname()))
    else: o['tr'].append((m(t.GetStart().x),m(t.GetStart().y),m(t.GetEnd().x),m(t.GetEnd().y),m(t.GetWidth()),t.GetLayerName(),t.GetNetname()))
for z in b.Zones():
    for L in (0,2):
        if z.IsOnLayer(L) and z.IsFilled():
            ps=z.GetFilledPolysList(L)
            for i in range(ps.OutlineCount()):
                ol=ps.Outline(i);o['z'].append((z.GetNetname(),L,[(m(ol.CPoint(j).x),m(ol.CPoint(j).y)) for j in range(ol.PointCount())]))
json.dump(o,open('/tmp/c/pl.json','w'))
