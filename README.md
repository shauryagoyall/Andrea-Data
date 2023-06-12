# mPFC-analysis

## Overview of scripts
**analyzeBehavior.ipynb**: started writing in 2020 to analyze behavioral data for the cue-reward association task. Primary plots consist of: trial accuracy by training day, arm selection over time, and trial accuracy by cue type. Rewrote from scratch in 2023 to make code modular.

**analyzeBehavior-old.ipynb**: copied old version when making the modular version from scratch in 2023. Will delete after I update with arm selection over time and any other things that are missing.

**supplemental_data.py**: data that I didn't want to store in a csv or include in the code.

**utils.py**: modular functions.

**accuracySimple.ipynb**: made in 2022 as a simpler version of the performance plot from analyzeBehavior. Instead of using the raw trial outcomes, it uses the calculated percentages which are in a separete csv. As I improve analyzeBehavior it should become obsolete.

**positionTracking.ipynb**: made in January 2023 to analyze tracking data.
