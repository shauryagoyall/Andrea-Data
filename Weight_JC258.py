#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:58:04 2021

@author: andrea
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

weight_JC258 = [
    436, #pre-op
    434, #post-op
    435,
    401,
    393,
    399,
    397,
    389,
    400,
]

starting_weight = weight_JC258[0]
weight85 = int(starting_weight*0.85)
weight80 = int(starting_weight*0.80)
print(' 80% weight: ',weight80,'\n','85% weight: ', weight85)

date_JC258 = [
    datetime.date(2021, 6, 7),
    datetime.date(2021, 6, 8),
    datetime.date(2021, 6, 9),
    datetime.date(2021, 6, 10),
    datetime.date(2021, 6, 11),
    datetime.date(2021, 6, 12),
    datetime.date(2021, 6, 13),
    datetime.date(2021, 6, 14),
    datetime.date(2021, 6, 15),
]

days = mdates.DayLocator() # find every day

amountfed_JC258 = [
]

fig, ax = plt.subplots(figsize=(12,8))
ax.plot(date_JC258, weight_JC258, marker='o', markersize=10, color="black")
ax.axhline(weight85, color='#cc0000', linewidth='3')
ax.axhline(weight80, color='#a6a6a6', linewidth='3', linestyle=':', alpha=0.5)
ax.set_ylim(starting_weight*0.7, starting_weight*1.05)
ax.set_ylabel("Weight (g)", fontsize=15)
ax.set_title("JC258 weight", fontsize=25)
ax.tick_params(axis='x', labelsize=15, rotation=50)
ax.tick_params(axis='y', labelsize=15)
ax.xaxis.set_major_locator(days) # set ticks to plot each day

ax2 = ax.twinx()
ax2.set_ylabel("% of original weight", fontsize=15)
ax2.set_ylim(70, 105)
ax2.tick_params(axis='y', labelsize=15)
fmt = '%.0f%%'
yticks = mtick.FormatStrFormatter(fmt)
ax2.yaxis.set_major_formatter(yticks)

ax2.yaxis.grid(True,which='both')

#plt.show()
plt.savefig("Weight_JC258.jpg")
