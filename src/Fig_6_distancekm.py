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

fig6raw = pd.read_excel(xls/"distance_kms.xlsx")



data = fig6raw
# lowercase
data.columns = [c.lower() for c in data.columns]
# make a datetime index
data['yr'] = data['year'].apply(lambda x: '1/1/' + str(x))
data['year'] = pd.to_datetime(data['yr'], infer_datetime_format=True)
data.set_index('year', inplace=True)
data.index = pd.to_datetime(data.index, format='%Y').year


# Figure Refugees relative to origin and residence country population (%): 1980-2018

sns.set_context('paper')
plt.style.use('seaborn-ticks')

cols=['mean_all', 'mean_fixed_origin', 'mean_fixed_residence']
linestijl=['solid', 'dotted', 'dashed']
labels = ['Mean of all countries', 'Fixed set origin countries', 'Fixed set residence countries']
colors = ['#e41a1c', 'blue', 'green']



fig, ax = plt.subplots(nrows=1, ncols=1, sharex='col', sharey='row')
for (c, kleur, ls, lab) in zip(cols, colors, linestijl, labels): 
    ax.plot(data.index, data[c], color=kleur, linestyle=ls, label=lab)


# annotations/legend
leg = plt.legend(loc='best', ncol=1, mode="expand", shadow=True, fancybox=True)
ax.set_ylim([0,3000])
ax.set_ylabel('Distance in km', fontstyle='italic', fontweight='light')


# range in years.
xranger = list(range(1980, 2016, 5))
xranger[0] = 1980
xranger = xranger+[2018]

ax.grid(which='major', axis='y', linestyle=':')
ax.set_xlim([1980, 2018])
ax.set_xticks(xranger)
sns.despine()

fig.suptitle(
    'Average geographical distance (in km): 1980 - 2018', y=1.05, x=0.5)
# footnotes
plt.figtext(x=0, y=0, s="Source: UNHCR population statistics database, authors’ calculations.",
            fontsize='small', fontstyle='italic', fontweight='light', color='gray')

# save
plt.savefig(graphs/"Fig6_ref_distance.svg",
            transparent=True, bbox_inches='tight', pad_inches=0)

plt.show()


