import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import datetime

from supplemental_data import cscheme

def import_data(datadir, animal):
    """
    Takes the data directory and animal name in format JC2xx as an input, and imports the data 
    from a csv file into a dataframe.

    Parameters
    ----------
    datadir : the directory that contains the csv files for each animal.
    animal : a string with the animal name in JC2xx format.

    Returns
    -------
    data : a dictionary of dataframes with data for each animal.
    
    """
    
    path = datadir+animal+'_data.csv'
    data = pd.read_csv(path)
    
    return data


def get_accuracy(data, animal):
    """
    Returns an array of trial accuracy (% trials correct) by training day.

    Parameters
    ----------
    data : a dictionary of dataframes with data for each animal.
    animal : a string with the animal name in JC2xx format.

    Returns
    -------
    accuracy : returns a dictionary of series with accuracy for each animals.

    """

    # group data by training days
    df = data[animal] # call the dataframe for that animal
    df_grouped = df.groupby('Session_ID')
    
    # for each day, divide the correct trials over the total trials
    correct = df_grouped['CorrectBool'].sum() # count correct trials in each day
    total = df_grouped['CorrectBool'].count() # count total trials in each day
    accuracy = np.round(correct/total*100, 2)
    
    return accuracy

def get_accuracy_by_cue(data, animal):
    """
    Returns an array of trial accuracy by training day by food cue type.

    Parameters
    ----------
    data : a dictionary of dataframes with data for each animal.
    animal : a string with the animal name in JC2xx format.

    Returns
    -------
    accuracy : returns a dictionary of series with accuracy for each animals.

    """

    # group data by training days
    df = data[animal] # call the dataframe for that animal
    df_grouped = df.groupby(['Session_ID', 'Flavor'])
    
    correct = df_grouped['CorrectBool'].sum()
    total = df_grouped['CorrectBool'].count()
    accuracy = np.round(correct/total*100, 2)
    
    return accuracy


def plot_accuracy(data, animal, ndays=None, title='[set title]', fig=None, ax=None):
    """
    Generates plots with animal accuracy over training days.

    Parameters
    ----------
    data : a dictionary of dataframes with data for each animal; *should already specify the animal* (possibly fix later).
    animal : a string with the animal name in JC2xx format.
    ndays : number of days to plot. The default is the length of the data.
    title : the title. If none, will prompt you to set a title.
    fig, ax : In case I want to define externally, otherwise the function will use default settings.

    Returns
    -------
    A plot.

    """
    
    # Default figure settings if not defined
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=(22,11))
    elif fig is not None and ax is None:
        ax = fig.add_subplot(111)
    
    # Set number of days to plot and x- and y-lims
    if ndays is None:
        ndays = len(data)
    
    # Title and axis formatting
    ax.set_title(title, fontsize=50, y=1.03)
    ax.set_xlabel("Training day", fontsize=30)
    ax.set_ylabel("Accuracy", fontsize=30)
    
    ax.set_xlim(-0.5,ndays+0.5)
    ax.set_ylim(-5,105)
    
    ax.tick_params(labelsize=30)
    ax.xaxis.set_major_locator(mtick.MultipleLocator(1)) # show each training day on the x-axis
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%')) # format the accuracy on the y-axis
    
    ax.axhline(y = 80, c='k', ls='--', linewidth=3, zorder=0) # zorder ensures that the line is below the animal accuracy lines
    ax.yaxis.grid(True)
    
    plt.plot(data, color=cscheme[animal], linewidth=4, marker='o', markersize=10, label=animal)
    ax.legend(loc=4, fontsize=30, framealpha=1)
   
    
def plot_accuracy_by_cue(data_by_cue, animal, cues, ndays, ax=None):
    """
    Plots accuracy by cue type, either individually or in multiple subplots.

    Parameters
    ----------
    data_by_cue : a dataframe of accuracy grouped by training day and cue type.
    animal : a string with the animal name in JC2xx format.
    cues : an array of cues used for each animal.
    ndays: number of days to plot.
    ax : axis in case I want to plot multiple plots and refer to them. The default is None.

    Returns
    -------
    A plot.

    """
    
    # Default figure settings if not defined
    if ax is None:
        fig, ax = plt.subplots(figsize=(15,8))
    
    # Title and axis formatting
    ax.set_title(animal, fontsize=30)
    ax.set_xlabel("Training day", fontsize=30)
    ax.set_ylabel("Accuracy", fontsize=30)
    ax.set_xlim(-0.5, ndays+0.5)
    ax.set_ylim(-5,105)
    ax.tick_params(labelsize=30)
    ax.xaxis.set_major_locator(mtick.MultipleLocator(1)) # show each training day on the x-axis
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%')) # format the accuracy on the y-axis
    ax.axhline(y = 80, c='k', ls='--', linewidth=3, zorder=0) # zorder ensures that the line is below the animal accuracy lines
    ax.yaxis.grid(True)
    
    for cue in cues:
        ax.plot(data_by_cue.loc[:, cue], color=cscheme[cue], linewidth=3, marker='o', markersize=8, label=cue)
    
    plt.tight_layout()
   
    
def save_fig(title, fmt='png'):
    """
    Saves figure under a specific title (converts whitespaces to underscores) and format (default is png).

    Parameters
    ----------
    title : a string with the title
    fmt : image format. The default is 'png'.

    Returns
    -------
    A saved figure.

    """
    title_no_spaces = '_'.join(title.split())
    timestamp = datetime.datetime.today().strftime("%Y-%m-%d-%H%M%S")
    if fmt=='png':
        plt.savefig(title_no_spaces+"_"+timestamp+".png")
    elif fmt=='svg':
        plt.savefig(title_no_spaces+"_"+timestamp+".svg")
    elif fmt =='jpg':
        plt.savefig(title_no_spaces+"_"+timestamp+".jpg")