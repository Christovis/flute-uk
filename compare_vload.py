import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

def GammaDistribution(x, alpha, beta, shift=0):
    return beta**alpha * (x-shift)**(alpha-1) * np.exp(-beta*(x-shift)) / gamma(alpha)

# parameters obtained from their R code
alpha = 2.115779
beta = 0.6898583
shift = -2.306691

plt.figure()
plt.plot(np.linspace(shift, 8, 100), 100.*GammaDistribution(np.linspace(shift, 8, 100), alpha, beta, shift))
plt.axvline(0, alpha=0.3, color='k', linewidth=1)
plt.xlim([-3, 9])
plt.xlabel('Days after symptom onset')
plt.ylabel('Density (%)')

print GammaDistribution(np.linspace(-2, 15, 16), alpha, beta, shift) * 9./0.21

plt.show()

