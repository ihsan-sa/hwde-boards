import pcbnew,sys
exec(open('/tmp/c/helpers.py').read())
PR[0]=70
zone("+SYS","F.Cu",[(44.9,52.8,48.65,54.0)])
f=pcbnew.ZONE_FILLER(b);f.Fill(b.Zones());b.Save(P);print('ok')
