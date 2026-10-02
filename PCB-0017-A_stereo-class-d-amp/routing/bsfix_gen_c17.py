import pcbnew,json
b=pcbnew.LoadBoard("kicad/PCB-0017-A_astra-amp.kicad_pcb")
mm=lambda v: round(pcbnew.ToMM(v),3)
rip=[]
for t in b.GetTracks():
    if t.Type()!=pcbnew.PCB_TRACE_T: continue
    n=t.GetNetname(); xs=(mm(t.GetStart().x),mm(t.GetEnd().x))
    if n=="/BSNR" and max(xs)>30.95: rip.append(str(t.m_Uuid.AsString()))
    if n=="/OUTNR" and min(xs)>=30.9 and max(xs)<=36.3: rip.append(str(t.m_Uuid.AsString()))
json.dump({"version":1,"ops":[{"op":"remove","uuid":u} for u in rip]},open("routing/bsfix_rip_c17.json","w"),indent=1)
json.dump({"version":1,"ops":[{"op":"place","ref":"C17","x":33.0,"y":26.85,"deg":90}]},open("routing/bsfix_move_c17.json","w"),indent=1)
W=0.624
def tr(a,b_,w,net): return {"op":"add_track","start":list(a),"end":list(b_),"width":w,"layer":"F.Cu","net":net}
ops=[tr((30.9,25.37),(31.2,25.6),W,"/OUTNR"),tr((31.2,25.6),(32.6,25.6),W,"/OUTNR"),
     tr((33.4,25.85),(35.0,25.85),W,"/OUTNR"),tr((35.0,25.85),(36.28,26.7),W,"/OUTNR"),
     tr((30.9,26.02),(31.7,26.75),0.2,"/BSNR"),tr((31.7,26.75),(32.7,27.85),0.2,"/BSNR")]
json.dump({"version":1,"ops":ops},open("routing/bsfix_route_c17.json","w"),indent=1)
print(len(rip),"rips")
