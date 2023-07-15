# -*- coding: utf-8 -*-
"""
Created on Sun May 10 21:55:26 2020

@author: ayjez
"""
#%%
import numpy as my
import pandas as pd
from numpy.random import randn

from scipy import stats

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
#%%
dataset1 = randn(100)

#plt.hist(dataset1)

dataset2 = randn(80)

#plt.hist(dataset2, color='indianred')

plt.hist(dataset1, density=True, color='indianred', alpha=0.5, bins=20)
plt.hist(dataset2, density=True, alpha=0.5, bins=20)

data1 = randn(1000)
data2 = randn(1000)

print("Plotting")
#sns.jointplot(data1, data2)
sns.jointplot(data1, data2, kind='hex')

plt.show()
# %%
