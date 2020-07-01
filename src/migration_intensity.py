    
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
from funcs import reformat_large_tick_values
import matplotlib.ticker as tick
from dateutil.relativedelta import relativedelta
import matplotlib as mpl
from matplotlib import lines





root = Path.cwd()
dta = root/"data/dta"
xls = root/"data/xls"
raw= root/"data/raw"
graphs = root/"manuscript/graphs"

#read in data

#emigration

intensity_emigration = pd.read_excel(xls/"Immigration and emigration intensities by region.xlsx", sheet_name='Emigration_intensity')


#lowercase
intensity_emigration.columns= [c.lower().strip() for c in intensity_emigration.columns]
cols=[ c for c in intensity_emigration.columns if 'emi_' in c or 'year' in c]
#relevant cols
intensity_emigration=intensity_emigration[cols]

#immigration

intensity_immigration = pd.read_excel(xls/"Immigration and emigration intensities by region.xlsx", sheet_name='Immigration_intensity')
intensity_immigration.columns= [c.lower().strip() for c in intensity_immigration.columns]
#select relevant cols
cols=[ c for c in intensity_immigration.columns if 'immi_' in c or 'year' in c]


intensity_immigration=intensity_immigration[cols]
#emigration
#make  datetimeindex. 
intensity_emigration['yr'] = intensity_emigration['year'].apply(lambda x: '1/1/' + str(x))
intensity_emigration['year'] = pd.to_datetime(intensity_emigration['yr'], infer_datetime_format=True)
intensity_emigration=intensity_emigration.set_index(['year']).drop(columns='yr')
#unstack
intensity_emigration.columns=[c.replace('emi_', '').capitalize() for c in intensity_emigration.columns]
#intensity_emigration.columns=[('emi_', '') for c in intensity_emigration.columns]

emigration=pd.DataFrame(intensity_emigration.unstack(), columns=['emigration_int'])
emigration = emigration.rename_axis(['region','year']).sort_index()


##immigration
#make datetimeindex
intensity_immigration['yr'] = intensity_immigration['year'].apply(lambda x: '1/1/' + str(x))
intensity_immigration['year'] = pd.to_datetime(intensity_immigration['yr'], infer_datetime_format=True)
intensity_immigration=intensity_immigration.set_index(['year']).drop(columns='yr')

#unstack
intensity_immigration.columns=[c.replace('immi_', '').capitalize() for c in intensity_immigration.columns]
immigration=pd.DataFrame(intensity_immigration.unstack(), columns=['immigration_int'])
immigration = immigration.rename_axis(['region','year']).sort_index()




data=pd.concat([emigration, immigration], axis=1, join='outer')




####### new version 
ord_regio=['Asia', 'Africa', 'Europe', 'Americas', 'Oceania']
id_emi=list(range(1,15,3))
id_immi=list(range(2, 15,3))
title_id=list(range(0,15,3))
idx=pd.IndexSlice

# build a rectangle in axes coords
left, width = .25, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

sns.set_context('paper')

fig, axs=plt.subplots(nrows=15, ncols=1, sharex='col', sharey='row', gridspec_kw={'hspace':0, 'wspace':0}, figsize=(9,6))

#emigration
for (i,r) in zip(id_emi, ord_regio):
    sel=data.loc[idx[r,:],:].droplevel(0)
    axs[i].plot(sel.index, sel['emigration_int'], color='#8dd3c7', linestyle='solid')
    axs[i].fill_between(sel.index,sel['emigration_int'], color='#8dd3c7', alpha=0.4)
    axs[i].set_ylim([0,1.5])
    axs[i].yaxis.set_major_formatter(tick.PercentFormatter(xmax=100))
#immigration
for (i,r) in zip(id_immi, ord_regio):
    sel=data.loc[idx[r,:],:].droplevel(0)
    axs[i].plot(sel.index, sel['immigration_int'], color='#bebada', linestyle='solid')
    axs[i].fill_between(sel.index,sel['immigration_int'], color='#bebada', alpha=0.4)
    axs[i].set_ylim([0,1.5])
    axs[i].yaxis.set_major_formatter(tick.PercentFormatter(xmax=100))
    axs[i].invert_yaxis()

#title
for (i,r) in zip(title_id, ord_regio):
    axs[i].text(x=0.5, y=0.5,s=r,transform=axs[i].transAxes)
    axs[i].spines['left'].set_visible(False)
    axs[i].yaxis.set_visible(False)



#layout all subplots
for ax in fig.axes: 
    ax.axes.get_xaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
#bottom time-axis
axs[-1].xaxis.set_visible(True)
axs[-1].spines['bottom'].set_visible(True)
axs[-1].tick_params(axis='x', length=2, labelsize='large')

plt.savefig(graphs/"Figx_emi_immi_intensity_mirrored.svg",
            transparent=True, bbox_inches='tight')

    


