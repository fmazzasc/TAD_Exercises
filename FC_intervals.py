import gammapy.stats as gstats 
import numpy as np 
from scipy import stats
import matplotlib.pyplot as plt
# if not installed, pip install gammapy 

meas_mean = 3.69999
std_dev = 1.5
alpha_list = [0.6827, 0.90, 0.95]
color_list = ["g-", "r-", "b-"]

x_bins = np.linspace(-3, 11,1000)
mu_bins = np.linspace(0, 8, 100)
for color, alpha in zip(color_list, alpha_list):
    up_list= []
    low_list = []
    print("Building FC acceptance intervals...")
    for mu in mu_bins:
        up, low = gstats.fc_find_acceptance_interval_gauss(mu, std_dev, x_bins, alpha)
        up_list.append(up)
        low_list.append(low)

    up_ci = gstats.fc_find_limit(meas_mean, up_list, mu_bins)
    low_ci = gstats.fc_find_limit(meas_mean, low_list, mu_bins)
    print("Alpha: ", alpha, ", Confidence interval: ", np.round((low_ci, up_ci), 2) )
    plt.plot(up_list, mu_bins, color, label =f"CL: {alpha}")
    plt.plot(low_list, mu_bins, color)

plt.legend()
plt.xlabel("Measured mean")
plt.ylabel(r"$\mu$")
plt.xlim(-2,4)
plt.ylim(0,7)
plt.grid()
plt.savefig("plots/FC_intervals.pdf")