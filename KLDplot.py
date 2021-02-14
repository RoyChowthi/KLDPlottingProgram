# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 12:11:28 2020

Guided KL-Divergence (KLD) application 
- define KLD function (or use existing)
- import data set
- generate subset of data for heurstic analysis (1M samples) 
- plot amplitude to find packet boundary
- generate data bins for KLD input 
- generate vector of relative entropy (KLD) values 
- plot KLD and analyze graph 
- determine KLD threshold for packet boundary
- implement packet counter for KLD output
- repeat process on full data set (16M samples)

@author: memcmanu
"""
# libraries needed 
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal,misc
from scipy import stats
import statistics

# define KLD function (or use existing)
def cross_entropy(X, Y):
    return sum(X * np.log2(X / Y)) 
# can define your own based on project specifications or use scipy.stats.entropy 
#   - these methods are different but will provide the same analysis 



# import data set
filename = 'EE559_datasets/set_12.txt'
set_1 = np.fromfile(filename,dtype=np.complex64)
setsize = np.size(set_1)
print(setsize)


# generate subset of data for heurstic analysis (1M samples) 
onemilsamps= set_1

# plot amplitude to find packet boundary
# - manually increase "inc" by 1 to scan all values 
# - may have to try "inc" in range (0,40)
x = np.real(onemilsamps)
y = np.imag(onemilsamps)
amp = np.sqrt(x**2 + y**2)
ran = list(range(0,len(amp))) # preserve x-axis indices
inc = 0 # index of plotted window
frame = 999999 # number of samples to plot per window 
plt.figure(0)
plt.plot(ran[inc*frame:(inc+1)*frame],amp[inc*frame:(inc+1)*frame],c='red')
plt.title('Capture sequence, amplitude')
plt.show()

# generate data bins for KLD input 
sample_size = 311 # number of IQ or AMP values per sample
set_size = int(len(onemilsamps)/sample_size) # number of samples per bin
seq_a = np.zeros((set_size,sample_size),dtype=np.float32)
for i in range (0, set_size):
    j = i +1
    sub = amp[i*sample_size: j*sample_size]
    seq_a[i,:] = np.array(sub)



# generate vector of relative entropy (KLD) values 
kl_set = np.zeros((set_size-1,1))

for i in range (0,set_size-1):
    kl_set[i] = cross_entropy(seq_a[i], seq_a[i + 1]) - cross_entropy(seq_a[i], seq_a[i])
    kl_val = kl_set[i]
    

pkts = 0
mini = min(kl_set);
for i in range (0,set_size-1):
    kl_vals = kl_set[i]
    if (kl_vals <= 0.6):
        pkts = pkts + 1

print(pkts)

# plot KLD and analyze graph 
plt.figure(1)
plt.plot(kl_set)
plt.title('KLD')
plt.show()

# implement packet counter for KLD output


        


