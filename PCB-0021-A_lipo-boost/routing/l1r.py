import pcbnew,sys
P=sys.argv[1];b=pcbnew.LoadBoard(P)
l1=b.FindFootprintByReference('L1'); r=l1.Reference(); p=l1.GetPosition()
r.SetPosition(pcbnew.VECTOR2I(p.x, p.y-int(float(sys.argv[2])*1e6)))
print(pcbnew.SaveBoard(P,b))
