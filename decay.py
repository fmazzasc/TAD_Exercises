import numpy as np
from ROOT import TCanvas, TH1D, TF1
import matplotlib.pyplot as plt

N0 = 5000
alpha = 0.01
t_start = 0
t_stop = 100
delta_t = 1

t_arr = np.arange(t_start, t_stop, delta_t)
prob_dec = alpha*delta_t
expo = TF1("expo", "[0]*exp(-x*[1])", t_start, t_stop, 2)
expo.SetParameters(N0, alpha)
expo.SetParNames("norm", "coeff")
histo = TH1D("h1", "Remaining nuclei; time(s); Counts", len(t_arr), t_start, t_stop)

N_t = []
for i, _ in enumerate(t_arr):
    N0 = np.sum(np.random.rand(N0) > prob_dec)
    histo.SetBinContent(i+1, N0)
canv = TCanvas("decay")
canv.cd()
histo.Draw()
expo.Draw("same")
canv.Draw()
input()
