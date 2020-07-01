import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
from funcs import reformat_large_tick_values
import matplotlib.ticker as tick
from dateutil.relativedelta import relativedelta

# paths
root = Path.cwd()
dta = root/"data/dta"
xls = root/"data/xls"
graphs = root/"manuscript/graphs"

#aw = pd.read_excel(xls/"by_gdp.xlsx")
sheet_names=['Absolute_origin','Absolute_destination', 'Percentages_origin', 'Percentages_destination']


raw={}
for sheet in sheet_names: 
    raw[f'{sheet}']= pd.read_excel(xls/"by_gdp.xlsx", sheet_name=sheet)
    raw[f'{sheet}'].columns=[c.strip().replace(' ', '_').lower() for c in raw[f'{sheet}']]
    raw[f'{sheet}']['yr']= raw[f'{sheet}']['year'].apply(lambda x: '1/1/' + str(x))
    raw[f'{sheet}']['year']= pd.to_datetime(raw[f'{sheet}']['yr'], infer_datetime_format=True)
    raw[f'{sheet}'].set_index('year', inplace=True)
    raw[f'{sheet}'].index = pd.to_datetime(raw[f'{sheet}'].index, format='%Y').year
    raw[f'{sheet}']=raw[f'{sheet}'].drop(columns='yr')

    


raw['Absolute_origin']=raw['Absolute_origin'].add_prefix('orig_')
raw['Absolute_destination']=raw['Absolute_destination'].add_prefix('dest_')

absolute=pd.concat([raw['Absolute_origin'],raw['Absolute_destination']], axis=1) 

origincols=[c for c in absolute.columns if 'orig' in c]
destcols=[c for c in absolute.columns if 'dest' in c]
linestyles=['-', '--', ':']
colors=['#e7298a','#66a61e','#e6ab02']
maxyear = absolute.index.max()
####plot for absolute nrs 
fig, (orig, dest)=plt.subplots(nrows=2, ncols=1)
orig.set_title('Refugees by origin country GDP per capita')
dest.set_title('Refugees by destination country GDP per capita')
for (c, ls, cl) in zip(origincols, linestyles,colors):
    orig.plot(absolute[c].index, absolute[c], color=cl, linestyle=ls)
    #add labels orig.text(x=maxyear, y=absolute.at[maxyear, c], s=lab, color=cl)
    

    
plt.show()
