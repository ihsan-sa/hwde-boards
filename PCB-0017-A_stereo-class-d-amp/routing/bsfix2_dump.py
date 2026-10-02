import pcbnew,sys
b=pcbnew.LoadBoard(sys.argv[1] if len(sys.argv)>1 else "kicad/PCB-0017-A_stereo-class-d-amp.kicad_pcb")
def mm(v): return round(pcbnew.ToMM(v),3)
X0,X1,Y0,Y1=29,41,23,41
for fp in b.GetFootprints():
    p=fp.GetPosition()
    if not (X0<=mm(p.x)<=X1 and Y0<=mm(p.y)<=Y1): continue
    bb=fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
    print("FP",fp.GetReference(),mm(p.x),mm(p.y),fp.GetOrientationDegrees(),"crt",mm(bb.GetLeft()),mm(bb.GetTop()),mm(bb.GetRight()),mm(bb.GetBottom()))
    for pd in fp.Pads():
        pp=pd.GetPosition(); bx=pd.GetBoundingBox()
        if fp.GetReference()=="U1" and not (X0<=mm(pp.x)): continue
        print("  pad",pd.GetNumber(),pd.GetNetname(),mm(pp.x),mm(pp.y),"box",mm(bx.GetLeft()),mm(bx.GetTop()),mm(bx.GetRight()),mm(bx.GetBottom()))
for t in b.GetTracks():
    s=t.GetStart();e=t.GetEnd()
    if not ((X0<=mm(s.x)<=X1 and Y0<=mm(s.y)<=Y1) or (X0<=mm(e.x)<=X1 and Y0<=mm(e.y)<=Y1)): continue
    kind="VIA" if t.Type()==pcbnew.PCB_VIA_T else "TRK"
    print(kind,t.GetNetname(),t.GetLayerName() if kind=="TRK" else "", mm(s.x),mm(s.y),mm(e.x),mm(e.y),mm(t.GetWidth()),t.m_Uuid.AsString())
ds=b.GetDesignSettings()
print("clearance default",mm(ds.m_NetSettings.GetDefaultNetclass().GetClearance()))
