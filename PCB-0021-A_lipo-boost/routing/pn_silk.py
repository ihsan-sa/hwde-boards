# Adds the part-number silkscreen line the boards repo requires on every board.
import pcbnew,sys
P=sys.argv[1];b=pcbnew.LoadBoard(P)
t=pcbnew.PCB_TEXT(b);t.SetText('PCB-0021 REV A');t.SetLayer(pcbnew.F_SilkS)
t.SetPosition(pcbnew.VECTOR2I(int(float(sys.argv[2])*1e6),int(float(sys.argv[3])*1e6)));t.SetTextSize(pcbnew.VECTOR2I(int(1.0e6),int(1.0e6)));t.SetTextThickness(int(0.15e6))
b.Add(t);print(pcbnew.SaveBoard(P,b))
