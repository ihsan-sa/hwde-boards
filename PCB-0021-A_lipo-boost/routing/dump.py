import pcbnew,sys,collections
b=pcbnew.LoadBoard(sys.argv[1])
m=lambda v:v/1e6
nets=collections.defaultdict(list)
for f in b.GetFootprints():
    for p in f.Pads():
        nets[p.GetNetname()].append((f.GetReference(),p.GetNumber(),round(m(p.GetX()),2),round(m(p.GetY()),2),p.GetLayerName() if False else ('T' if p.IsOnLayer(0) else 'B'),round(m(p.GetSizeX()),2),round(m(p.GetSizeY()),2)))
for n,l in sorted(nets.items()): print(n,l)
print(len(b.GetTracks()))
bb=b.GetBoardEdgesBoundingBox();print(m(bb.GetX()),m(bb.GetY()),m(bb.GetRight()),m(bb.GetBottom()))
print([ (z.GetNetname(),z.GetLayerName(),z.GetAssignedPriority()) for z in b.Zones()])
