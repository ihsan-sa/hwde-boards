import pcbnew,sys
P=sys.argv[1];b=pcbnew.LoadBoard(P)
iu=lambda v:int(round(v*1e6))
b.FindFootprintByReference('L1').Move(pcbnew.VECTOR2I(iu(-0.6),0))
for t in list(b.GetTracks()):
    if t.GetNetname() in('/CHG','/PGOOD'): b.Remove(t)
for z in list(b.Zones()):
    if z.GetNetname()=='+SYS' and z.GetAssignedPriority() in (16,17,42,43): b.Remove(z)
b.Save(P)
