# epfix: rewrite U1's EP thermal-via array (pad "33" thru_hole) from 3x3 @1.0 mm to 4x4 @0.9 mm,
# in the library footprint and in the board's U1 instance. Run once from the workspace root.
import re, uuid
coords=[-1.35,-0.45,0.45,1.35]
p='lib/aiee.pretty/HTSSOP-32_L11.0-W6.1-P0.65-LS8.1-BL-EP.kicad_mod'
s=open(p).read()
old=re.findall(r'\t\(pad "33" thru_hole circle[^\n]*\n',s); assert len(old)==9
new=''.join(f'\t(pad "33" thru_hole circle (at {x:.2f} {y:.2f}) (size 0.61 0.61) (drill 0.30) (layers *.Cu))\n' for y in coords for x in coords)
first=s.find(old[0]); last=s.find(old[-1])+len(old[-1]); assert s[first:last]==''.join(old)
open(p,'w').write(s[:first]+new+s[last:])
p='kicad/PCB-0017-A_stereo-class-d-amp.kicad_pcb'
s=open(p).read()
blocks=list(re.finditer(r'\t\t\(pad "33" thru_hole circle\n\t\t\t\(at ([-\d.]+) ([-\d.]+) 270\)\n\t\t\t\(size 0.61 0.61\)\n\t\t\t\(drill 0.3\)\n\t\t\t\(layers "\*\.Cu"\)\n\t\t\t\(remove_unused_layers no\)\n\t\t\t\(net "GND"\)\n\t\t\t\(uuid "[^"]+"\)\n\t\t\)\n',s)); assert len(blocks)==9
blk=lambda x,y:'\t\t(pad "33" thru_hole circle\n\t\t\t(at %g %g 270)\n\t\t\t(size 0.61 0.61)\n\t\t\t(drill 0.3)\n\t\t\t(layers "*.Cu")\n\t\t\t(remove_unused_layers no)\n\t\t\t(net "GND")\n\t\t\t(uuid "%s")\n\t\t)\n'%(x,y,uuid.uuid4())
new=''.join(blk(x,y) for y in coords for x in coords)
first=blocks[0].start(); out=s
for b in reversed(blocks): out=out[:b.start()]+out[b.end():]
open(p,'w').write(out[:first]+new+out[first:])
