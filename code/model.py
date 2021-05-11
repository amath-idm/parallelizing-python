'''
Create an intentionally slow model
'''

import numpy as np
import pylab as pl
import sciris as sc


class SIR(sc.prettyobj):
    '''
    A simple SIR model with noise.

    Args:
        beta (float): infection rate
        gamma (float): recovery rate
        npts (int): number of days
        N (float): population size
        noise (float): noise level
        seed (int): random seed
    '''

    def __init__(self, beta=2e-4, gamma=1e-4, npts=2e5, N=1e3, noise=30, seed=1):
        self.beta  = beta
        self.gamma = gamma
        self.npts  = int(npts)
        self.N     = N
        self.noise = noise
        self.seed  = int(seed)
        self.initialize()
        return


    def initialize(self):
        np.random.seed(self.seed)
        self.S = np.full(self.npts+1, np.nan)
        self.I = np.full(self.npts+1, np.nan)
        self.R = np.full(self.npts+1, np.nan)
        self.S[0] = self.N-1
        self.I[0] = 1
        self.tvec = np.arange(self.npts+1)
        return


    def run(self):
        r_beta  = self.noise*np.random.randn(self.npts)
        r_gamma = self.noise*np.random.randn(self.npts)
        for t in np.arange(self.npts):
            S = self.S[t]
            I = self.I[t]
            R = self.R[t]
            infections = self.beta*S*I/self.N*(1 + r_beta[t])
            recoveries = self.gamma*I*(1 + r_gamma[t])
            S = S - infections
            I = I + infections - recoveries
            R = R + recoveries
            self.S[t+1] = S
            self.I[t+1] = I
            self.R[t+1] = R
        return


    def plot(self):
        fig = pl.figure()
        pl.plot(self.tvec, self.S, label='S')
        pl.plot(self.tvec, self.I, label='I')
        pl.plot(self.tvec, self.R, label='R')
        pl.xlabel('Time')
        pl.ylabel('People')
        pl.legend()
        pl.show()
        return fig


def run_sir(**kwargs):
    ''' Helper function to run the SIR model '''
    print(f'Running {kwargs}...')
    sir = SIR(**kwargs)
    sir.run()
    return sir


if __name__ == '__main__':
    sc.tic()
    sir = SIR()
    sir.run()
    sir.plot()
    sc.toc()
    pl.savefig('example-sir.png', dpi=200)
    print(sir)