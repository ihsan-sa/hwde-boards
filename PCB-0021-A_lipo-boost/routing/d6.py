import pcbnew,sys
exec(open('/tmp/c/helpers.py').read())
z=pcbnew.ZONE(b);z.SetLayer(b.GetLayerID("F.Cu"));z.SetNet(net("+SYS"));z.SetAssignedPriority(80)
z.SetMinThickness(iu(0.2));z.SetLocalClearance(iu(0.2));z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
o=z.Outline();o.NewOutline()
for x,y in((44.9,52.8),(48.65,52.8),(48.65,57.0),(47.85,57.0),(47.85,54.0),(44.9,54.0)):o.Append(iu(x),iu(y))
b.Add(z)
f=pcbnew.ZONE_FILLER(b);f.Fill(b.Zones());b.Save(P);print('ok')
