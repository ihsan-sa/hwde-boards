import pcbnew,sys
P=sys.argv[1];b=pcbnew.LoadBoard(P)
for z in list(b.Zones()):
    if z.GetNetname()=='+SYS' and z.GetAssignedPriority() in (26,71): b.Remove(z)
b.Save(P)
