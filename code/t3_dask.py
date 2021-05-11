'''
Tool 3: Dask
'''

import pylab as pl
import numpy as np
import sciris as sc
from model import run_sir
import dask
from dask.distributed import Client


def run_dask(seed, beta):
    sir = run_sir(seed=seed, beta=beta)
    return sir

if __name__ == '__main__':

    # Initialization
    n_runs = 10
    seeds = np.arange(n_runs)
    betas = np.linspace(0.5e-4, 5e-4, n_runs)

    # Run
    sc.tic()
    client = Client(n_workers=n_runs)
    queued = []
    for r in range(n_runs):
        run = dask.delayed(run_dask)(seeds[r], betas[r])
        queued.append(run)
    sirlist = list(dask.compute(*queued))
    sc.toc()

    # Plot
    pl.figure()
    colors = sc.vectocolor(betas, cmap='turbo')
    for r in range(n_runs):
        pl.plot(sirlist[0].tvec, sirlist[r].I, c=colors[r], label=f'beta={betas[r]:0.2g}')
    pl.legend()
    pl.show()
    pl.savefig('example-multiprocessing.png', dpi=300)
