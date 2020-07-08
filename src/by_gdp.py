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
labels=['Low GDP', 'Medium GDP', 'High GDP']
destcols=[c for c in absolute.columns if 'dest' in c]
linestyles=['--','-', ':']
colors=['#1b9e77','#d95f02','#e7298a']
maxyear = absolute.index.max()
####plot for absolute nrs 
sns.set_context('paper')
fig, (orig, dest)=plt.subplots(nrows=2, ncols=1)
orig.set_title('Refugees by origin country GDP per capita', loc='left')
dest.set_title('Refugees by destination country GDP per capita', loc='left')

#origin
for (c, ls, cl, lab) in zip(origincols, linestyles,colors, labels):
    orig.plot(absolute[c].index, absolute[c], color=cl, linestyle=ls)
    #add labels
    orig.text(x=maxyear+0.5, y=absolute.at[maxyear, c], s=lab, color=cl)
  
#destination
for (c, ls, cl, lab) in zip(destcols, linestyles,colors, labels):
    dest.plot(absolute[c].index, absolute[c], color=cl, linestyle=ls)
    #add labels
    dest.text(x=maxyear+0.5, y=absolute.at[maxyear, c], s=lab, color=cl)

#all axes: 
for ax in fig.axes:
    sns.despine(ax=ax)
    ax.set_xlim([1980, 2018])
    ax.yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))
    ax.set_ylim(0,10000000)



plt.subplots_adjust(hspace=0.5)
fig.savefig(graphs/'figx_absolute_byGDP.svg', transparent=True, bbox_inches='tight')


#relative percentages
raw['Percentages_origin']=raw['Percentages_origin'].add_prefix('orig_')
raw['Percentages_destination']=raw['Percentages_destination'].add_prefix('dest_')

percent=pd.concat([raw['Percentages_origin'],raw['Percentages_destination']], axis=1) 


origincols=[c for c in percent.columns if 'orig' in c]
origincols_r=[c for c in reversed(origincols)]


labels=['Low GDP', 'Medium GDP', 'High GDP']
labels_r=[c for c in reversed(labels)]
destcols=[c for c in percent.columns if 'dest' in c]
destcols_r=[c for c in reversed(destcols)]

linestyles=['--','-', ':']
linestyles_r=[c for c in reversed(linestyles)]
colors=['#1b9e77','#d95f02','#e7298a']
colors_r=[c for c in reversed(colors)]
maxyear = percent.index.max()

# build a rectangle in axes coords
left, width = .25, .5
bottom, height = .25, .5
right = left + width
top = bottom + height


widths = [2, 2, 0.5]

sns.set_context('paper')
fig, axs=plt.subplots(nrows=3, ncols=3, sharex='col', sharey='row', gridspec_kw={'width_ratios': widths})
titlesaxs=axs[0,2], axs[1,2], axs[2,2]
originaxs=axs[0,0], axs[1,0], axs[2,0]
destaxs=axs[0,1], axs[1,1], axs[2,1]
#titles
for (ax, cl, lb) in zip(titlesaxs, colors, labels): 
    ax.text(0.5 * (left + right), 0.5 * (bottom + top), lb, color=cl,
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes)
    ax.axis('off')
#origin
#coltitles
axs[0,0].set_title('Refugees (%)\nby origin country GDP', loc='left')
for (ax, c, ls, cl, lab) in zip(originaxs, origincols, linestyles,colors, labels):
    ax.plot(percent[c].index, percent[c], color=cl, linestyle=ls)
    ax.fill_between(percent[c].index,percent[c], color=cl, alpha=0.4)


#destination
#coltitles
axs[0,1].set_title('Refugees (%)\nby destination country GDP', loc='left')
for (ax, c, ls, cl, lab) in zip(destaxs, destcols, linestyles,colors, labels):
    ax.plot(percent[c].index, percent[c], color=cl, linestyle=ls)
    ax.fill_between(percent[c].index,percent[c], color=cl, alpha=0.4)


#all
for ax in fig.axes: 
    sns.despine(ax=ax)
    ax.yaxis.set_major_formatter(tick.PercentFormatter(xmax=1))
    ax.set_ylim([0, 0.04])
    ax.set_xticks([1980, 2000, 2018])

fig.savefig(graphs/'figx_percentage_refugees_byGDP.svg', transparent=True, bbox_inches='tight')

plt.show()

