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
        self.S = [self.N-1]
        self.I = [1]
        self.R = [0]
        self.tvec = np.arange(self.npts+1)
        return


    def run(self):
        r1 = self.noise*np.random.randn(self.npts)
        r2 = self.noise*np.random.randn(self.npts)
        for t in np.arange(self.npts):
            S = self.S[-1]
            I = self.I[-1]
            R = self.R[-1]
            infections = self.beta*S*I/self.N*(1 + r1[t])
            recoveries = self.gamma*I*(1 + r2[t])
            S = S - infections
            I = I + infections - recoveries
            R = R + recoveries
            self.S.append(S)
            self.I.append(I)
            self.R.append(R)
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


def run_sir(*args, **kwargs):
    ''' Helper function to run the SIR model '''
    print(f'Running {args} {kwargs}...')
    sir = SIR(*args, **kwargs)
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