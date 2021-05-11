'''
Tool 1: multiprocessing
'''

import numpy as np
import pylab as pl
import sciris as sc
import multiprocessing as mp
from model import run_sir

def run_multiprocessing(args):
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
    multipool = mp.Pool(processes=mp.cpu_count())
    sirlist = multipool.map(run_multiprocessing, inputlist)
    multipool.close()
    multipool.join()
    sc.toc()

    # Plot
    pl.figure()
    colors = sc.vectocolor(betas, cmap='turbo')
    for r in range(n_runs):
        pl.plot(sirlist[0].tvec, sirlist[r].I, c=colors[r], label=f'beta={betas[r]:0.2g}')
    pl.legend()
    pl.show()
    pl.savefig('example-multiprocessing.png', dpi=300)
