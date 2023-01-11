import numpy as np
import matplotlib.pyplot as plt

f = np.loadtxt('JC274-20220312.whl')
x1 = f[:,0] # primary LED
y1 = f[:,1] # primary LED
x2 = f[:,2] # secondary LED, inactive
y2 = f[:,3] # secondary LED, inactive
timestamps = f[:,4]
valid = f[:,5] # binary that indicates if record is valid or not

print(timestamps)

###

plt.scatter(x1, y1, alpha=0.5)
plt.show()

