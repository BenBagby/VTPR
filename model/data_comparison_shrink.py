import matplotlib.pyplot as plt
from pandas import read_csv, DataFrame
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from numpy import sqrt 

filenames = [
    "shrink_DS1_lower20_BP_forced_lowVT",
    "shrink_DS1_lower20_BP_forced_highVT",
    "shrink_DS1_lower20_BP_not_forced_highVT",
    "shrink_DS1_lower20_BP_not_forced_lowVT"
]

for filename in filenames:

    data = read_csv(filename + ".csv",usecols = ['shrinkage', 'eos_shrink'])

    data = data.dropna()
    data['perdiff'] = abs(data['shrinkage'] - data['eos_shrink'])/(data['shrinkage']/2 + data['eos_shrink']/2) *100


    vmg = data['shrinkage']
    eos = data['eos_shrink']

    a = plt.axes(aspect = 'equal')

  
    plt.title(filename)
    sc = plt.scatter(vmg,eos,color = 'red', label = "model", marker = ',', s = 1)

    MAE = mean_absolute_error(vmg,eos)
    print(MAE)

    MSE = mean_squared_error(vmg,eos)
    RMSE = sqrt(MSE) 
    plt.xlabel('VMG Shrinkage')
    plt.ylabel('EOS Shrinkage')
    lims = [0.64,0.72]
    plt.xlim(lims)
    plt.ylim(lims)
    plt.plot(lims,lims)
    plt.annotate("MAE: {}".format(round(MAE,4)), xy = (0.1,0.9), xycoords = 'axes fraction')

    plt.savefig('shrink_graphs/' + filename + "_2")
    plt.close()




