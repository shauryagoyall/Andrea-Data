# mPFC-analysis

## Overview of scripts
**analyzeBehavior.ipynb**: main script to analyze behavioral data for the cue-reward association task. Primary plots consist of: trial accuracy by training day, arm selection over time, and trial accuracy by cue type.

**supplemental_data.py**: data that I didn't want to store in a csv or include in the code.

**utils.py**: modular functions.

**positionTracking.ipynb**: script to analyze tracking data and separate longer sessions into individual trials (in progress).

# Archived
**analyzeBehavior-old.ipynb**: copied old version when making the modular version from scratch in 2023. Will delete after I update with arm selection over time and any other things that are missing.

**accuracySimple.ipynb**: a simpler version of the performance plot from analyzeBehavior. Instead of using the raw trial outcomes, it uses the calculated percentages which are in a separete csv. As I improve analyzeBehavior it should become obsolete.
