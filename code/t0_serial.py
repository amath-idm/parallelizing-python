'''
Tool 0: Run in serial
'''

import numpy as np
import pylab as pl
import sciris as sc
from model import run_sir

if __name__ == '__main__':

    # Initialization
    n_runs = 10
    seeds = np.arange(n_runs)
    betas = np.linspace(0.5e-4, 5e-4, n_runs)

    # Run
    sc.tic()
    sirlist = []
    for r in range(n_runs):
        sir = run_sir(seed=seeds[r], beta=betas[r])
        sirlist.append(sir)
    sc.toc()

    # Plot
    pl.figure()
    colors = sc.vectocolor(betas, cmap='turbo')
    for r in range(n_runs):
        pl.plot(sirlist[0].tvec, sirlist[r].I, c=colors[r], label=f'beta={betas[r]:0.2g}')
    pl.legend()
    pl.show()