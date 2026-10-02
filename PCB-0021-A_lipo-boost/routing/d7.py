import pcbnew,sys
exec(open('/tmp/c/helpers.py').read())
PR[0]=90
zone("+SYS","B.Cu",[(47.95,54.5,48.55,56.8)])
via("+SYS",48.25,54.9);via("+SYS",48.25,56.55)
f=pcbnew.ZONE_FILLER(b);f.Fill(b.Zones());b.Save(P);print('ok')
