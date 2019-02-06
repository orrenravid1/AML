import math
import numpy as np
import matplotlib.pyplot as plt
import random

N = 20
threshold = 0.3
t_max = 8
times = np.linspace(0.0,t_max,num = N)
precision = .97

def thresh(t):
    return threshold + (1-threshold)*(1-t/t_max)**2

f = []

for time in times:
    f.append(thresh(time))
    
plt.plot(times,f)

plt.ylim([0,1])

plt.show()
