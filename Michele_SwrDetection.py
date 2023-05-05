# You need as input the power in the SWR band and the threshold. 
# I generally compute the power in time windows T of 200~300 ms with a short time fourier transform 
# (you can use scipy.signal.stft for example, or implement it, or use wavelets, your choice) on the eegh file. 
# Then I align it to the whl for ease (i.e. have an overlap of T - 25.6 ms, so you have one entry for the power 
# for each entry of the whl - makes life easier for indexing, speed etc...)

def SWR_det(swr_pow,thr): 
    SWR=[] # return [beginning, end, peak] of each event, in whl time indexes
    
    # add additional zero at the end
    swr_p = np.array(swr_pow,copy=True)
    swr_p = np.hstack([swr_p,0])
    # check when it is above / below threshold
    der= np.array(swr_p[1:]>thr,dtype=int) - np.array(swr_p[:-1]>thr,dtype=int) 
    # beginnings are where  der > 0
    begs=np.where(der>0)[0]+1
    last=0
    for beg in begs: # check each swr
        if beg > last: # not to overlap
            first = max(beg - 2,0) # include 50 ms before: usually a lot of spiking happens before high SWR power
            if np.min(swr_p[beg:beg+50]<0.8*thr): # just a sanity check - power after >1sec below threshold? 
                #if not, something might be wrong - maybe threshold too low!?
                last = beg+np.where(swr_p[beg:beg+50]<0.8*thr)[0][0] # end SWR where power is less 80% threshold
                peak = first + np.argmax(swr_p[first:last]) # detect peak power
                if (3 < last - first < 30): # check length: should be between 75 and 750 ms, but you can change this at will
                    SWR.append([first,last,peak])
    return SWR