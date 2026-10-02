import pcbnew,sys
exec(open('/tmp/c/helpers.py').read())
zone("+SYS","F.Cu",[(46.4,52.9,48.0,54.0)])
zone("VBUS","F.Cu",[(34.65,49.3,35.65,51.2)])
via("GND",39.5,43.0);via("GND",40.5,44.5)
f=pcbnew.ZONE_FILLER(b);f.Fill(b.Zones());b.Save(P);print('ok')
