'''
Tool 5: concurrent.futures
'''

import pylab as pl
import numpy as np
import sciris as sc
from model import run_sir
import concurrent.futures as cf


def run_concurrent(args):
    seed, beta = args
    sir = run_sir(seed=seed, beta=beta)
    return sir

if __name__ == '__main__':

    # Initialization
    n_runs = 10
    seeds = np.arange(n_runs)
    betas = np.linspace(0.5e-4, 5e-4, n_runs)

    # Run
    sc.tic()
    inputlist = [(seed,beta) for seed,beta in zip(seeds, betas)]
    with cf.ProcessPoolExecutor() as executor:
        sirlist = list(executor.map(run_concurrent, inputlist))
    sc.toc()

    # Plot
    pl.figure()
    colors = sc.vectocolor(betas, cmap='turbo')
    for r in range(n_runs):
        pl.plot(sirlist[0].tvec, sirlist[r].I, c=colors[r], label=f'beta={betas[r]:0.2g}')
    pl.legend()
    pl.show()
    pl.savefig('example-concurrent.png', dpi=300)
