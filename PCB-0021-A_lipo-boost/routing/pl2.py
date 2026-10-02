import json,sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon
o=json.load(open('/tmp/c/pl.json'));x0,y0,x1,y1=map(float,sys.argv[2:6]);lay=sys.argv[6] if len(sys.argv)>6 else 'F.Cu'
L=0 if lay=='F.Cu' else 2
fig,ax=plt.subplots(figsize=(14,14*(y1-y0)/(x1-x0)))
cols={}
import hashlib
def c(n): return '#'+hashlib.md5(n.encode()).hexdigest()[:6]
for n,l,pts in o['z']:
    if l==L: ax.add_patch(Polygon(pts,fc=c(n),alpha=.25,ec=c(n),lw=.3))
for t in o['tr']:
    if t[5]==lay: ax.plot([t[0],t[2]],[t[1],t[3]],lw=t[4]*14*72/(x1-x0)*0.8,color=c(t[6]),solid_capstyle='round',alpha=.8)
for p in o['pads']:
    ax.add_patch(Rectangle((p[2],p[3]),p[4],p[5],fc='none',ec='k',lw=.6));ax.text(p[2]+p[4]/2,p[3]+p[5]/2,p[0]+'\n'+p[1],fontsize=4,ha='center',va='center')
for v in o['via']: ax.add_patch(plt.Circle((v[0],v[1]),.3,fc='none',ec='r'))
ax.set_xlim(x0,x1);ax.set_ylim(y1,y0);ax.set_aspect('equal');ax.grid(lw=.2)
plt.savefig(sys.argv[1],dpi=110,bbox_inches='tight')
