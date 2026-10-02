import pcbnew,json
b=pcbnew.LoadBoard("kicad/PCB-0017-A_stereo-class-d-amp.kicad_pcb")
mm=lambda v: round(pcbnew.ToMM(v),3)
rip=[]
def seg(t): return (mm(t.GetStart().x),mm(t.GetStart().y),mm(t.GetEnd().x),mm(t.GetEnd().y))
want12=[(29.72,32.736,30.084,33.1),(30.084,33.1,30.457,33.1),(31.5,33.1,30.457,33.1),(31.5,33.1,31.5,34.6),(31.5,34.6,30.498,34.6),(30.498,34.6,29.99,35.109),(29.99,35.109,29.9,35.109)]
def same(a,b_): return all(abs(x-y)<0.002 for x,y in zip(a,b_)) or all(abs(x-y)<0.002 for x,y in zip(a,(b_[2],b_[3],b_[0],b_[1])))
for t in b.GetTracks():
    n=t.GetNetname(); s=seg(t)
    if t.Type()==pcbnew.PCB_VIA_T:
        if n=="GND" and abs(s[0]-34.3)<0.01 and abs(s[1]-34.9)<0.01: rip.append(t)
        continue
    if t.Type()!=pcbnew.PCB_TRACE_T: continue
    xs=(s[0],s[2]); ys=(s[1],s[3])
    if n in("/BSNR","/BSPL","/BSNL") and max(xs)>30.95: rip.append(t)
    if n=="/OUTPL" and min(xs)>=30.9 and max(xs)<=36.33 and max(ys)<=32.65 and min(ys)<32.65: rip.append(t)
    if n=="/OUTNL" and min(xs)>=30.9 and max(xs)<=35.5 and min(ys)<=29.25: rip.append(t)
    if n=="+12V" and any(same(s,w) for w in want12): rip.append(t)
for t in rip: print("RIP",t.GetNetname(),seg(t))
json.dump({"version":1,"ops":[{"op":"remove","uuid":t.m_Uuid.AsString()} for t in rip]},open("routing/bsfix2_rip.json","w"),indent=1)
json.dump({"version":1,"ops":[{"op":"place","ref":r,"x":x,"y":y,"deg":d} for r,x,y,d in [("C17",33.9,26.85,90),("C16",33.6,30.8,-90),("C15",34.3,34.6,90),("C7",32.3,33.95,0),("C9",32.3,35.1,0),("C11",34.15,38.5,-90)]]},open("routing/bsfix2_move.json","w"),indent=1)
def tr(a,b_,w,net,layer="F.Cu"): return {"op":"add_track","start":list(a),"end":list(b_),"width":w,"layer":layer,"net":net}
def via(p,net): return {"op":"add_via","at":list(p),"size":0.6,"drill":0.3,"net":net}
def chain(pts,w,net,layer="F.Cu"): return [tr(pts[i],pts[i+1],w,net,layer) for i in range(len(pts)-1)]
W=0.624;P=0.882;S=0.2
ops=[]
ops+=chain([(30.9,26.02),(32.2,26.02),(32.9,26.72),(32.9,27.85),(33.9,27.85)],S,"/BSNR")
ops+=chain([(30.9,27.33),(31.35,27.2)],S,"/BSPL")+[via((31.35,27.2),"/BSPL")]+chain([(31.35,27.2),(34.9,29.8)],S,"/BSPL","B.Cu")+[via((34.9,29.8),"/BSPL")]+chain([(34.9,29.8),(33.6,29.8)],S,"/BSPL")
ops+=chain([(30.9,27.98),(31.9,27.98),(32.3,28.38),(32.3,31.5),(32.6,31.8),(33.6,31.8),(35.48,31.8),(36.33,32.65)],W,"/OUTPL")
ops+=chain([(30.9,29.28),(31.5,29.28),(31.5,33.0),(35.5,33.0),(35.5,39.9)],W,"/OUTNL")
ops+=chain([(30.9,29.93),(30.7,30.7)],S,"/BSNL")+[via((30.7,30.7),"/BSNL")]+chain([(30.7,30.7),(34.3,36.3)],S,"/BSNL","B.Cu")+[via((34.3,36.3),"/BSNL")]+chain([(34.3,36.3),(34.3,35.6)],S,"/BSNL")
ops+=chain([(29.72,32.736),(30.3,33.316),(30.934,33.95),(31.6,33.95),(31.6,35.1),(29.9,35.109)],P,"+12V")
json.dump({"version":1,"ops":ops},open("routing/bsfix2_route.json","w"),indent=1)
print(len(rip),"rips",len(ops),"route ops")
