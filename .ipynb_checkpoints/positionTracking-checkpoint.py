#!/usr/bin/env python
# coding: utf-8

# ## JC274-20220314 .whl metadata
# Animal: **JC274** <br>
# Chocolate_arm: **8** <br>
# Honey_arm: **4** <br>
# Sunflower_arm: 5 (not relevant for this session) <br>
# ---
# Training_day: **8** <br>
# Accuracy: **64.29%** <br>
# Threshold_reached_day: **10** <br>

# In[3]:

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime

import IPython
print(IPython.sys_info())
# mpl.use('Qt5Agg')
mpl.use('TkAgg')

# plt.ion()


basename = 'JC283-20220920'
timenow = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")

pos = pd.read_csv(basename+'.whl', sep=" ",
                 header=None,
                 names=["x1","y1","x2","y2","timestamps","valid"])


pos[pos == 1023] = np.nan # replace 1023 (error value) with NaN

x1 = pos["x1"]
y1 = pos["y1"]
timestamps = pos["timestamps"]

fig, ax = plt.subplots(figsize=(8,8))
ax.plot(x1, y1, linewidth=1)
ax.set_title(basename+" tracking", fontsize=18, y=1.01)
ax.tick_params(labelsize=14)
plt.xlim(0,160)
plt.ylim(0,160)
plt.show()
# plt.savefig(basename+"_tracking_"+timenow+".png")

# print(timestamps.min(), timestamps.max())
# print(timestamps.count())

# timestart = 0
# timeend = 1_030_000
# subset = pos.loc[(timestamps > timestart) & (timestamps < timeend)]
#
# fig, ax = plt.subplots(figsize=(8,8))
# ax.plot(subset["x1"], subset["y1"], linewidth=1)
# ax.set_title(basename+" tracking subset", fontsize=18, y=1.01)
# ax.tick_params(labelsize=14)
# plt.xlim(0,160)
# plt.ylim(0,160)
# plt.show()
## plt.savefig(basename+"_tracking-subset_"+timenow+".png")