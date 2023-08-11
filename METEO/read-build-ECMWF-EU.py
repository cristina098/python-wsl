import requests
import json
import datetime
import numpy as np
import pandas as pd
import seaborn as sb

import matplotlib.pyplot as plt

plt.style.use('ggplot')


firstDate = '2023-07-21T21:00:00'
lastDate = '2023-08-11T15:00:00'
timeHelper = (datetime.datetime.strptime(lastDate, '%Y-%m-%dT%H:%M:%S') - datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S'))

filesNo = 1 + (timeHelper.days*24 + timeHelper.seconds//3600) // 6

print(f"You have {filesNo} ECMWF-EU files")

############################################################################ read first file to build df structure
f = open(f'/home/lali/TITAN-ROG-sync/python/METEO/ECMWF-EU-{firstDate}.json',)
data = json.load(f)
f.close()

nowTime = datetime.datetime.strptime(data['RO']['now'], '%Y-%m-%dT%H:%M:%S')
nowTemp = data['RO']['temp']

allData = pd.DataFrame(columns = ['Date', 'Real'])
for i in range(len(data['ECMWFEU'])):
    prognosisTime = datetime.datetime.strptime(data['ECMWFEU'][i]['now'], '%Y-%m-%dT%H:%M:%S')
    prognosisTemp = data['ECMWFEU'][i]['temp']
    deltaTime = prognosisTime - nowTime
    diferenta = deltaTime.days*24 + deltaTime.seconds//3600
    allData[diferenta] = []

newRowDict = {'Date':firstDate}
newRowDF = pd.DataFrame([newRowDict])
allData = pd.concat([allData, newRowDF])
for i in range(filesNo + len(data['ECMWFEU'])):
    intermDate = datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=6*(i+1))
    newRowDict = {'Date':intermDate.isoformat()}
    newRowDF = pd.DataFrame([newRowDict])
    #newRowDF.reset_index(drop=True, inplace=True)
    #allData.reset_index(drop=True, inplace=True)
    allData = pd.concat([allData, newRowDF])
    allData.reset_index(drop=True, inplace=True)

allData = allData.set_index('Date')
#print(allData)
##################################################################### df ready

for i in range(filesNo):
    fileTime = (datetime.datetime.strptime(firstDate, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=6*i)).isoformat()
    f = open(f'/home/lali/TITAN-ROG-sync/python/METEO/ECMWF-EU-{fileTime}.json',)
    print(f"reading {fileTime}")
    data = json.load(f)
    f.close()
    allData.at[fileTime, 'Real'] = data['RO']['temp']
    nowTime = datetime.datetime.strptime(data['RO']['now'], '%Y-%m-%dT%H:%M:%S')
    for i in range(len(data['ECMWFEU'])):
        prognosisTime = datetime.datetime.strptime(data['ECMWFEU'][i]['now'], '%Y-%m-%dT%H:%M:%S')
        prognosisTemp = data['ECMWFEU'][i]['temp']
        deltaTime = prognosisTime - nowTime
        diferenta = deltaTime.days*24 + deltaTime.seconds//3600
        allData.at[data['ECMWFEU'][i]['now'], diferenta] = prognosisTemp

allDataDiff = allData.copy()
for index, row in allDataDiff.iterrows():
    for i in np.arange(0, 234, 6):
        allDataDiff.at[index, i] = allDataDiff.at[index, i] - allDataDiff.at[index, 'Real']

print(allDataDiff)

#allData.to_csv('/home/lali/TITAN-ROG-sync/python/METEO/MET-Norway.csv')
#allDataDiff.to_csv('/home/lali/TITAN-ROG-sync/python/METEO/MET-Norway-diff.csv')

if (True):
    if (False): #True pentru diferenta
        allDataDiffPlot = allDataDiff.replace(np.nan,0)
        del allDataDiffPlot['Real']
        ax = sb.heatmap(allDataDiffPlot, annot = False, linewidths = .5, cmap="vlag", vmin=-8, vmax=8)
    else:
        allDataPlot = allData.replace(np.nan,0)
        ax = sb.heatmap(allDataPlot, annot = False, linewidths = .5, cmap="vlag")
    plt.show()