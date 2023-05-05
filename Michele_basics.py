## basics: load clu and res, compute speed and heading, compute rate maps
## you can use this as a library or copy/paste the scripts you need
## notice that they are optimized for whls that go from -1 to 150 max 
### -> if you need something bigger change those parameters and / or change bin size (automatically set to 3cm)

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as nd
from skimage.restoration import denoise_bilateral
from statsmodels.nonparametric.kernel_density import KDEMultivariate

### load clu and res - this is NOT suited for reading e.g. whl files, for that use np.loadtxt!
def read_integers(filename): # faster way of reading clu / res
    with open(filename) as f:
        return np.array([int(x) for x in f])

### bin spikes (aligned with whl - i.e. 25.6 ms time windows)
def bindata(clu,res):
    bindata = np.zeros([clu[0]+2, int(res[-1]/512)+1])
    for ir, r in enumerate(res):
        bindata[clu[ir+1], int(r/512)] += 1
    return bindata

### compute speed - simple moving average
def comp_speed(whl): #compute speed from the whl - use it for filtering!
    temp = np.zeros(whl.shape[0])
    speed = np.zeros(whl.shape[0])
    for i in range(5,whl.shape[0]-5):
        if whl[i,0] > 0 and whl[i+1,0] > 0 and whl[i,1] > 0 and whl[i+1,1] > 0:
            temp[i] = np.sqrt((whl[i,0] - whl[i+1,0])**2 + (whl[i,1] - whl[i+1,1])**2)
        else:
            temp[i]=-1
    # smooth using a moving average
    for i in range(5,whl.shape[0]-5):
        t = temp[i-5:i+5]
        t = t[t>=0]
        if len(t)>0 and whl[i,0]>0:
            speed[i] = np.mean(t)
        else:
        	speed[i]=np.nan
    return speed*39.0625
    
### compute heading - also here simple moving average    
from scipy.stats import circmean
def heading(whl):
    temp = np.zeros(whl.shape[0])
    heading = np.zeros(whl.shape[0])
    for i in range(whl.shape[0]-1):
        if whl[i,0] > 0 and whl[i+1,0] > 0 and whl[i,1] > 0 and whl[i+1,1] > 0:
            temp[i] = np.arctan2(whl[i+1,1] - whl[i,1], whl[i+1,0] - whl[i,0]) + np.pi
        else:
            temp[i]=-1000
    
    for i in range(5,whl.shape[0]-5):
        t = temp[i-5:i+5]
        t = t[t>-1000]
        if len(t)>0 and whl[i,0]>0:
            heading[i] = circmean(t)
        else:
            heading[i] = np.nan
    return heading
    
### Classical Gaussian firing rate estimate

def occmap_gauss(whl, # positions x,y over time
				 speed, # speed aligned with whl
				 spf): # speed filter

    # spf is the speed filter - anything between 3 and 9 is fine
    
    # again this goes from 0 to 150 cm, spatial bins of 3cm
    
    whl = np.floor(whl[speed > spf,:] / 3).astype(int)  # speed filter
    occ = np.zeros((50,50))
    for i in range(whl.shape[0]):
        if(-1 < whl[i,0]<50 and -1<whl[i,1]<50):
            occ[whl[i,0],whl[i,1]] += 1
    return occ/ 39.0625

# in the following you'll need a list of times, aligned with the whl, where a certain cell has fired
# if you have the spikes binned, you can do that by using something like this:
# spkl = np.concatenate([np.where(binned_data[cell]>i)[0] for i in range(10)])

def rate_gauss(occ, # occupancy map
			   whl, # positions x,y
			   spkl, # list of times, aligned with whl, when cell spiked
			   speed, # speed
			   spf, # speed filter
			   sigma_gauss=0): # sigma for smoothing

    # sigma gauss is the amount of gaussian smoothing to apply - usually between 1 and 3
	# if you use this method then compute the occupancy with occmap_gauss ;)
    rate = np.zeros((50,50)) # again this goes from 0 to 150 cm, spatial bins of 3cm
    spkl = spkl[speed[spkl]>spf] # speed filter
    spkp = np.floor(whl[spkl,:] / 3).astype(int) # positions where the spikes "happened"
    for i in range(spkp.shape[0]):
        if(-1<spkp[i,0]<50 and -1<spkp[i,1]<50):
            rate[spkp[i,0],spkp[i,1]] +=1
    # divide by occupancy
    rate[occ>0.05] = rate[occ>0.05] / occ[occ>0.05] # 0.05 means 50 ms occupancy - change this threshold if you want/need!
    # smoothing - watch out, if there are gaps in the behavior this will introduce small biases!
    if sigma_gauss > 0: 
        rate=nd.gaussian_filter(rate,sigma=sigma_gauss)
    
    rate[occ==0]=np.nan # delete places where occupancy is zero
    return rate


### Kernel density estimation of firing rate with triweight kernel
### this code is written for environemnts 150cm large and 3cm bins
### change parameters if you need more or less!

def sn(h,k): #squared norm
    y = h - k
    return y.T[0]**2 + y.T[1]**2

def K(x,z,sig): #triweight kernel
    
    nss = 9*sig**2 #9 sigma squared
    snp = 1 - sn(x,z) / nss #1 - squared norm points / 9 sigma squared
    snp[snp<0] = 0
    
    return 4 / (np.pi * nss) * snp**3

def occmap(whl, speed=None,spf=None,sigma_ker=4.2,del_low_occ=True,): #occupancy map
    if spf:
        whl = np.array(whl[speed > spf,:])
    occ = np.zeros((50,50))
    for i in range(50): 
        for j in range(50):
            occ[i,j] = np.sum(K(np.array((1.5 + i*3, 1.5 + j*3)),whl,sigma_ker))
    if del_low_occ:  
	    occ[occ<np.max(occ)/1000]=0 #cut out bins with low coverage, < 0.1% of peak
    return occ

# you'll need here a list of times, aligned with the whl, where a certain cell has fired
# if you have the spikes binned, you can do that by using something like:
# spkl = np.concatenate([np.where(binned_data[cell]>i)[0] for i in range(10)])

def ratemap(occ,whl,spkl,speed,spf,sigma_ker=4.2,sigma_gauss=1,denoise=False,del_low_occ=True,occ_thr=0.05): #firing rate
    rate = np.zeros((50,50))
    if len(spkl) > 0:
        spkl = np.array(spkl[speed[spkl]>spf])
        spkp = np.array(whl[spkl,:])
        for i in range(50): 
            for j in range(50):
                if(occ[i,j] > occ_thr): #avoid problems at locations with low coverage...
                    rate[i,j] = np.sum(K(np.array((1.5 + i*3, 1.5 + j*3)),spkp,sigma_ker)) / occ[i,j]
        if sigma_gauss > 0: # add gaussian smoothing on top
            rate = nd.gaussian_filter(rate,sigma=sigma_gauss)
        if denoise: # use a denoise algorithm
            rate = denoise_bilateral(rate, sigma_color=np.max(r)/10, sigma_spatial=15,multichannel=False)
        if del_low_occ: # eliminate place with low occupancy
            rate[occ==0]=0
    return rate

