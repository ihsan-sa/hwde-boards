import pcbnew,sys
b=pcbnew.LoadBoard("kicad/PCB-0017-A_stereo-class-d-amp.kicad_pcb")
def mm(v): return round(pcbnew.ToMM(v),3)
for fp in b.GetFootprints():
    r=fp.GetReference()
    if r in ("C15","C16","C17","C7","C9","C18","L1","L2","L3","L4","U1"):
        p=fp.GetPosition(); print("FP",r,mm(p.x),mm(p.y),fp.GetOrientationDegrees(),fp.GetFPID().GetLibItemName())
        for pd in fp.Pads():
            n=pd.GetNetname(); pp=pd.GetPosition(); s=pd.GetSize()
            if r!="U1" or (20<=int(pd.GetNumber() or 0)<=28 if pd.GetNumber().isdigit() else False):
                print("  pad",pd.GetNumber(),n,mm(pp.x),mm(pp.y),mm(s.x),mm(s.y))
nets=("/OUTNR","/BSNR","/OUTPL","/BSPL","/OUTNL","/BSNL","/OUTPR","/BSPR")
for t in b.GetTracks():
    n=t.GetNetname()
    s=t.GetStart();e=t.GetEnd()
    inreg = 28<=mm(s.x)<=41 and 21<=mm(s.y)<=34
    if n in nets or (inreg and n in ("+12V",)):
        kind="VIA" if t.Type()==pcbnew.PCB_VIA_T else "TRK"
        print(kind,n,t.GetLayerName() if kind=="TRK" else "", mm(s.x),mm(s.y),mm(e.x),mm(e.y),mm(t.GetWidth()))
