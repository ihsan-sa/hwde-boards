import pcbnew,sys
P=sys.argv[1];b=pcbnew.LoadBoard(P)
iu=lambda v:int(round(v*1e6))
b.FindFootprintByReference('L1').Move(pcbnew.VECTOR2I(iu(-0.6),0))
dead=[t for t in b.GetTracks() if t.GetNetname() in('/CHG','/PGOOD')]
print('rm',len(dead))
for t in dead: b.Delete(t)
for z in list(b.Zones()):
    if z.GetNetname()=='+SYS' and z.GetAssignedPriority() in (16,17,42,43): b.Remove(z)
print(pcbnew.SaveBoard(P,b))
