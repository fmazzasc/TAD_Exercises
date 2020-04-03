import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
# if not installed, pip3 install iminuit

############helper function####################


def correlation_from_covariance(covariance):
    v = np.sqrt(np.diag(covariance))
    outer_v = np.outer(v, v)
    correlation = covariance / outer_v
    correlation[covariance == 0] = 0
    return correlation
###############################################


# x = x0 + v0*t + 0.5*a*t**2
x = np.array([10, 23, 39.3, 30, 50, 60, 80, 90, 100, 110])
t = np.array([0, 0.485, 0.91, 0.7, 1.150,
              1.350, 1.710, 1.865, 2.020, 2.150])
sigma_x = np.array([0.11, 0.16, 0.19, 0.21, 0.24,
                    0.26, 0.31, 0.32, 0.34, 0.36])

# building the matrix to invert
matrix = np.zeros((3, 3))
# setting the columns
matrix[:, 0] = [np.sum(t**i/sigma_x**2) for i in (4, 3, 2)]
matrix[:, 1] = [np.sum(t**i/sigma_x**2) for i in (3, 2, 1)]
matrix[:, 2] = [np.sum(t**i/sigma_x**2) for i in (2, 1, 0)]
vec = [np.sum(t**i*x/sigma_x**2) for i in [2, 1, 0]]

# we need to find params in matrix * params = vec
# inverting the matrix and find the parameters
params = np.linalg.solve(matrix, vec)
matrix_inv = np.linalg.inv(matrix)
print("\n--------------------------------------------------------------")
print("Fit parameters \n")
print("a [cm/s^2]: ", round(2*params[0], 2),
      " +- ", round(2*np.sqrt(matrix_inv[0][0]), 2))
print("v0 [cm/s]: ", round(params[1], 2), " +- ",
      round(np.sqrt(matrix_inv[1][1]), 2))
print("x0 [cm]: ", round(params[2], 2), " +- ",
      round(np.sqrt(matrix_inv[2][2]), 2))

print("\n--------------------------------------------------------------")
print("Correlation matrix\n")
print(np.round(correlation_from_covariance(matrix_inv), 2))


# evaluating position at t == 1s
print("\n--------------------------------------------------------------")
print("Position at t=1s \n")
t_ev = 1
position = params[0] + params[1] + params[2]
error2 = matrix_inv[0, 0] + matrix_inv[1, 1] + matrix_inv[2,
                                                          2] + 2*(matrix_inv[0, 1] + matrix_inv[0, 2]+matrix_inv[1, 2])
error = np.sqrt(error2)
print("x(t=1s): ", round(position, 2), " +- ", round(error, 2))


print("\n--------------------------------------------------------------")
print("Comparison using Minuit \n")


def least_squares_np(par):
    mu = np.polyval(par, t)
    return np.sum((x - mu) ** 2 / sigma_x**2)
print(least_squares_np(params))

m = Minuit.from_array_func(least_squares_np, (3, 3, 3),
                           error=(0.01, 0.01, 0.01), errordef=1)
m.migrad()
print("a [cm/s^2]: ", round(2*m.values["x0"], 2),
      " +- ", round(2*m.errors["x0"], 2))
print("v0 [cm/s]: ", round(m.values["x1"], 2),
      " +- ", round(m.errors["x1"], 2))
print("x0 [cm]: ", round(m.values["x2"], 2), " +- ", round(m.errors["x2"], 2))
print("\n--------------------------------------------------------------")
x_pol = np.linspace(0, 2.3, 1000)
plt.errorbar(t, x, yerr=sigma_x, fmt="r.", label="data")
plt.plot(x_pol, np.polyval(params, x_pol), 'g-',
         label="Fit(manual, Minuit, np.polyfit)")
plt.legend()
plt.grid()
plt.ylabel("x(cm)")
plt.xlabel("t(s)")
plt.text(x=0.0, y=100, s=r"$\chi^2$ / NDF = {}/{}".format(round(least_squares_np(params),1), len(x)-len(params)))

plt.savefig("plots/least_squares.pdf")