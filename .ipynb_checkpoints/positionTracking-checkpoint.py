import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import the data
f = np.loadtxt('JC274-20220312.whl')
x1 = f[:,0] # primary LED
y1 = f[:,1] # primary LED
x2 = f[:,2] # secondary LED, inactive
y2 = f[:,3] # secondary LED, inactive
timestamps = f[:,4]
valid = f[:,5] # binary that indicates if record is valid or not

###

# convert to df; first make a dictionary, then convert
df_dict = {"x1": x1, "y1": y1,"x2": x2, "y2": y2, "timestamps": timestamps, "valid": valid}
df = pd.DataFrame(df_dict)
df[df == 1023] = np.nan # replace 1023 (error value) with NaN
print(df.describe())

###

plt.scatter(df.loc[:,"x1"], df.loc[:,"y1"], alpha=0.5)
plt.show()
