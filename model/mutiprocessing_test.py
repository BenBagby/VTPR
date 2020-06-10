from VTPR import VTPR as EOS
from pandas import read_csv, DataFrame
import pandas as pd
import numpy as np


from multiprocessing import Pool

import time



all_data = read_csv("data/Shrink_DS1_lower20.csv",
usecols = [
    'PRESSURE',
    'TEMP',
    'N2',
    'C1',
    'CO2',
    'C2',
    'C3',
    'IC4',
    'NC4',
    'IC5',
    'NC5',
    'C6',
    'c7*',
    'Hypo  Specific Gravity',
    'Hypo  Molecular Weight',
    'shrinkage'
    ])

component_list = [
    'Nitrogen', 
    'Methane', 
    'Carbon Dioxide', 
    'Ethane', 
    'Propane', 
    'Isobutane', 
    'n-Butane', 
    'Isopentane',
    'n-Pentane', 
    'n-Hexane', 
    'Heptanes+' 
]


def add_shrinkage(data):
    index_list = []
    shrink_list = []
    for index , row in data.iterrows():
        mole_per = [
            row['N2'],
            row['C1'],
            row['CO2'],
            row['C2'],
            row['C3'],
            row['IC4'],
            row['NC4'],
            row['IC5'],
            row['NC5'],
            row['C6'],
            row['c7*']
        ]
        mole_sum = sum(mole_per)

        mole_fraction = [x / mole_sum for x in mole_per]

        T = (row['TEMP']-32)*5/9+273.15 
        P = (row['PRESSURE'] +14.65)/14.5038

        MW_plus_fraction = row['Hypo  Molecular Weight']
        SG_plus_fraction = row['Hypo  Specific Gravity']
        vmg_shrink = row['shrinkage']
        
        if np.isnan(T) == False and np.isnan(P) == False:
            #PR(component_list, mole_fraction, P, T).bubble_graph(filename = str(index), graph_feedP = True)
            print(index)
            print("VMG Shrink:", vmg_shrink)
            shrinkage = EOS(component_list, mole_fraction, MW_plus_fraction, SG_plus_fraction, P, T).shrinkage(bubble_point_force =False)
            print("EOS Shrink:", shrinkage,"\n")
            shrink_list.append(shrinkage)
            index_list.append(index)

    df_new = DataFrame(shrink_list, columns = ['eos_shrink'], index = index_list)
    return df_new


def paralellize_dataframe(df, func, n_cores = 4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df






if __name__ == '__main__':
    #for n_cores in range(8,12):
    n_cores = 3
    #start = time.time()
    df_new = paralellize_dataframe(all_data, add_shrinkage, n_cores = n_cores)
    #end = time.time()
    #elapsed = end - start
    #print("Multiprocess time, {} cores: {}".format(n_cores, elapsed/len(df_new.index)))
    print(df_new)
    all_data['eos_shrink'] = np.nan
    all_data.update(df_new)
    print(all_data)
    all_data.to_csv('test_output/shrink_DS1_lower20_BP_forced_lowVT.csv')