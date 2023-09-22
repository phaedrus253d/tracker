#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 23:13:56 2023

@author: trevor
"""

import pandas as pd 
from datetime import date, datetime, timedelta as td
import os
import sys
import imp

import json

# import fitbit
# import gather_keys_oauth2 as Oauth2
import numpy as np
# import pandas as pd 
# from datetime import date, datetime, timedelta as td
import dateutil.parser
import seaborn
import time

import requests
import arrow
from requests.auth import HTTPBasicAuth


import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

import warnings

import data_pull_atimelogger as logdp


warnings.filterwarnings("ignore")

START_DATE = (datetime.now() - pd.DateOffset(days=30)).strftime("%Y-%m-%d")
END_DATE =  (datetime.now() + pd.DateOffset(days=1)).strftime("%Y-%m-%d")
print(f'Data from {START_DATE} through {END_DATE}, not including the latest date.')

# If you stored your credentials in a different location, add the credentials path
#cred_path = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir)
#cpath = os.path.join(cred_path, 'DD')
repo_path = os.getcwd()

fsize = 18
params = {
    'axes.labelsize': fsize, 
    'axes.titlesize':fsize, 
    'axes.titlepad': 20,
    'xtick.labelsize':fsize,
    'xtick.major.pad': 5, 
    'ytick.labelsize':fsize,
    'axes.labelpad': 20,
    'lines.linewidth' : 3,
    'figure.titlesize': fsize *1.5,
    'figure.figsize' : (35,8),
    'legend.title_fontsize': fsize,
    'legend.fontsize': fsize #*0.925, 
} 
plt.rcParams.update(params) 
plt.close('all')


#%% atimelogger
with open(os.path.join(os.getcwd(),"credentials.json"), "r") as file:
    credentials = json.load(file)
    atimelogger_cr = credentials['atimelogger']
    USERNAME = atimelogger_cr['USERNAME']
    PASSWORD = atimelogger_cr['PASSWORD']

auth_header = HTTPBasicAuth(USERNAME, PASSWORD)

types_atimelogger_df = logdp.get_types(auth_header)
types_atimelogger_df.head(1)

entries_atimelogger_df = logdp.get_intervals(auth_header, 
                                             start_date = START_DATE, 
                                             end_date = END_DATE, 
                                             timezone = 'US/Eastern')

log_df = pd.merge(entries_atimelogger_df, types_atimelogger_df, left_on = 'type_id', right_on = 'guid')
log_df.head(1) 