import pcbnew,sys
P=sys.argv[1];b=pcbnew.LoadBoard(P)
zs=list(b.Zones())
for z in zs:
    if z.GetNetname()=='+SYS' and z.GetAssignedPriority()==23: b.Remove(z)
f=pcbnew.ZONE_FILLER(b);f.Fill(b.Zones());b.Save(P);print('ok')
