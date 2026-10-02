import pcbnew,sys
P=sys.argv[1];b=pcbnew.LoadBoard(P)
for t in b.GetTracks():
    if t.GetClass()=='PCB_VIA' and abs(t.GetX()/1e6-48.25)<.01 and abs(t.GetY()/1e6-56.55)<.01: t.SetPosition(pcbnew.VECTOR2I(int(48.25e6),int(56.85e6)))
f=pcbnew.ZONE_FILLER(b);f.Fill(b.Zones());b.Save(P)
