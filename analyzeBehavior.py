import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Import the data
JC240_data = pd.read_csv("JC240_data.csv")

# Explore the data
JC240_data.head() # show data = sanity check
JC240_data.info() # Index, data type, and memory information


# Split the data by Session ID
numTrials = JC240_data.groupby("Session_ID").size() # lists the number of trials per session
sessionID = JC240_data["Session_ID"].unique() # returns an array of unique session IDs
session1 = JC240_data.loc[df.Session_ID==1]

# trialOutcome =

numCorrectTrials = JC240_data.groupby("SessionID")

# apply(list)
