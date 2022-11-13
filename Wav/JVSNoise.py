import statsmodels.api as sm

y_lowess = sm.nonparametric.lowess(y, x, frac = 0.3)  # 30 % lowess smoothing

plt.plot(y_lowess[:, 0], y_lowess[:, 1], 'b')  # some noise removed
plt.show()
