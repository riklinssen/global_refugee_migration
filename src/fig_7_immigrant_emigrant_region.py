import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
from funcs import reformat_large_tick_values
import matplotlib.ticker as tick
from dateutil.relativedelta import relativedelta
import matplotlib as mpl

mpl.rc_file_defaults()
# paths
root = Path.cwd()
dta = root/"data/dta"
xls = root/"data/xls"
graphs = root/"manuscript/graphs"

####on absolute values

#load in raw data
im_raw=pd.read_excel(xls/"residence_origin_absolute_intensity.xlsx", sheet_name='immigration_abs')
#set multindex
immi=im_raw.set_index(['region', 'year']).sort_index()
#emigration
emi_raw=pd.read_excel(xls/"residence_origin_absolute_intensity.xlsx", sheet_name='emigration_abs')
emi=emi_raw.set_index(['region', 'year']).sort_index()

#data=df with region year multiindex. 

data=pd.concat([immi, emi], axis=1)

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
    axs[i].plot(sel.index, sel['emi_abs'], color='red', linestyle='solid')
    axs[i].fill_between(sel.index,sel['emi_abs'], color='red', alpha=0.4)
    axs[i].set_ylim([0,12000000])
    axs[i].yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))
#immigration
for (i,r) in zip(id_immi, ord_regio):
    sel=data.loc[idx[r,:],:].droplevel(0)
    axs[i].plot(sel.index, sel['immi_abs'], color='blue', linestyle='solid')
    axs[i].fill_between(sel.index,sel['immi_abs'], color='blue', alpha=0.4)
    axs[i].set_ylim([0,12000000])
    axs[i].yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))
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

plt.savefig(graphs/"Figx_immi_emi_absolute_mirrored.svg",
            transparent=True, bbox_inches='tight')

    

