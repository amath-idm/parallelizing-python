import pylab as pl
import sciris as sc
import datathief as dt


pl.rc('font', family='Proxima Nova')
pl.rc('figure', dpi=200)

fvert  = 'vertical-scaling-raw.png'
fhoriz = 'horizontal-scaling-raw.png'
outfile = 'scaling-cost.png'

xlim = [0, 450]
ylim = [0, 120]
vert = dt.datathief(fvert, xlim=xlim, ylim=ylim)

xlim = [0, 550]
ylim = [0, 50]
horiz = dt.datathief(fhoriz, xlim=xlim, ylim=ylim)


vcost = vert.y[-1]/vert.x[-1]
hcost = horiz.y[-1]/horiz.x[-1]

fig = pl.figure(figsize=(8,4))
pl.plot(vert.x, vert.y, label=f'Vertical scaling (${vcost:0.2f}/core)')
pl.plot(horiz.x, horiz.y, label=f'Horizontal scaling (${hcost:0.2f}/core)')
pl.xlabel('Number of cores')
pl.ylabel('Cost ($)')
pl.title('Typical Azure costs')
pl.legend()
pl.show()
pl.xlim(left=0)
pl.ylim(bottom=0)
pl.savefig(outfile, dpi=300)
sc.runcommand(f'trim {outfile}')