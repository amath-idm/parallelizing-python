'''
Tool 4: celery
'''

import pylab as pl
import numpy as np
import sciris as sc
from model import run_sir
from celery import Celery, group
import subprocess

app = Celery('code', include=['t4_celery'])
app.conf['CELERY_TASK_SERIALIZER'] = 'pickle'
app.conf['CELERY_RESULT_SERIALIZER'] = 'pickle'
app.conf['CELERY_ACCEPT_CONTENT'] = ['json', 'pickle']

@app.task
def run_celery(args):
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
    celery_cmdline = f'celery worker -A t4_celery -l INFO -c {n_runs}'.split(' ')
    subprocess.Popen(celery_cmdline)
    inputlist = [(seed,beta) for seed,beta in zip(seeds, betas)]
    jobs = group(run_celery.s(arg) for arg in inputlist)
    sirlist = jobs.apply_async()
    # worker = app.Worker(include=['t4_celery'])
    # app.start()
    sc.toc()

    # Plot
    pl.figure()
    colors = sc.vectocolor(betas, cmap='turbo')
    for r in range(n_runs):
        pl.plot(sirlist[0].tvec, sirlist[r].I, c=colors[r], label=f'beta={betas[r]:0.2g}')
    pl.legend()
    pl.show()
    pl.savefig('example-multiprocessing.png', dpi=300)
