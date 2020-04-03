import numpy as np
from ROOT import TCanvas, TH1D, TF1, gPad, gStyle, kGreen
from root_numpy import fill_hist

#########Settable parameters############
N_exp = 10000
N0 = 500
alpha = 2*10**-4
delta_t = 1
T = 100
#######################################

m = T/delta_t
beta = alpha*N0
inf = max(np.round(beta*T - 2*np.sqrt(beta*T)),0)
sup = max(np.round(beta*T + 2.5*np.sqrt(beta*T)),10)
histo = TH1D("h1", f"; # of decays(in {T}s); Counts", int(sup-inf), inf, sup)
N_dec = []
for i in range(N_exp):
    N_dec.append(np.sum(np.random.rand(int(m)) < beta*delta_t))


fill_hist(histo, N_dec)
poisson = TF1("f1", "[0]*TMath::Poisson(x,[1])", inf, sup)
poisson.SetTitle("Poisson distribution")
poisson.SetParameters(histo.Integral(), beta*T)

binomial = TF1("binomial", "[0]*TMath::Binomial([1], x) * ([2])^(int(x)) * (1-[2])^([1]-int(x))", inf, sup)
binomial.SetTitle("Binomial distribution")
binomial.SetNpx(int(sup-inf))
binomial.SetParameter(0, histo.Integral())
binomial.SetParameter(1, m)
print(beta*delta_t)
print(m)
binomial.SetParameter(2, beta*delta_t)
binomial.SetLineColor(kGreen)
canv = TCanvas()
canv.cd()
histo.Draw()
poisson.Draw("same")
binomial.Draw("same")
gPad.BuildLegend(0.3, 0.3, 0.6, 0.5)
gStyle.SetOptStat(0)
canv.Print("plots/n_decay.pdf")

