import numpy as np
from scipy.stats import norm, t

## Helper function to compute CI. If central== True central CI are computed, else upper and lower CI are computed
## If var == None the CI are computed using the tStudent distr with df degrees of freedom
###############################################################################################
def compute_conf_interval(alpha, x, samp_mean, samp_mean_dev, var=None, df=None, central=True):
    if central:
        low_val = (1-alpha)/2
        upp_val = (1+alpha)/2
    else:
        low_val = 1-alpha
        upp_val = alpha
    if var is not None:
        cdf_arr = norm.cdf(x, samp_mean, samp_mean_dev)
    else:
        x = (samp_mean-x)/(samp_mean_dev)
        x = x[::-1]
        cdf_arr = t.cdf(x, df)
    low_int = x[cdf_arr < low_val][-1]
    upp_int = x[cdf_arr > upp_val][0]
    if central:
        if var is not None:
            print("Alpha: ", alpha, "; Central CI (Gauss): ", np.round((low_int, upp_int),2))
        else:
            print("Alpha: ", alpha, "; Central CI (tStudent): ", np.round((samp_mean +
                                                                  low_int*samp_mean_dev, samp_mean + upp_int*samp_mean_dev),2))
    else:
        if var is not None:
            print("Alpha: ", alpha, "; Lower CI (Gauss): ", round(low_int,2))
            print("Alpha: ", alpha, "; Upper CI (Gauss): ", round(upp_int,2))
        else:
            print("Alpha: ", alpha, "; Lower CI: ",
                  round(samp_mean + low_int*samp_mean_dev,2))
            print("Alpha: ", alpha, "; Upper CI: ",
                  round(samp_mean + upp_int*samp_mean_dev,2))
############################################################################################

x = [2.2, 4.3, 1.7, 6.6]
dev = 3
samp_mean = np.mean(x)
samp_mean_dev = dev/np.sqrt(len(x))
arr = np.linspace(samp_mean-5*samp_mean_dev,
                  samp_mean + 5*samp_mean_dev, 10000)
print("Sample mean: ", round(samp_mean,2))
print("Standard deviation of the sample mean: ", samp_mean_dev)

###PART 1
print("--------------------------------------------")
print("Central confidence intervals\n")
alpha_list = [0.95, 0.90, 0.6827]
for alpha in alpha_list:
    compute_conf_interval(alpha, arr, samp_mean, samp_mean_dev, dev)

print("--------------------------------------------")
print("Upper and lower confidence intervals\n")
alpha_list = [0.95, 0.8413]
for alpha in alpha_list:
    compute_conf_interval(alpha, arr, samp_mean, samp_mean_dev, dev, central = False)

print("\nProbability to take a measurement < 0 : ", round(norm.cdf(0, samp_mean, dev),2))
print("Probability of mean <0 : ", round(norm.cdf(0, samp_mean, samp_mean_dev),2))



#### PART 2
print("--------------------------------------------")
print("FeldmanCousins confidence intervals\n")
# values inherited from the script FC_intervals.py
print("Alpha: 0.95", ", Confidence interval: ", [1.13, 6.71])
print("Alpha: 0.90", ", Confidence interval: ", [1.45, 6.22])
print("Alpha: 0.6827", ", Confidence interval: ", [2.26, 5.25])



#### PART 3
print("--------------------------------------------")
print("CI supposing variance == sample variance\n")
compute_conf_interval(0.95, arr, samp_mean, samp_mean_dev, samp_mean_dev)
print("\nCI supposing variance unknown\n")
compute_conf_interval(0.95, arr, samp_mean, samp_mean_dev, df=3)
print("--------------------------------------------")