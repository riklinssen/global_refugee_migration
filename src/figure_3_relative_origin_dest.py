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

fig3raw = pd.read_excel(xls/"Fig3_relative_origin_dest.xlsx")

data = fig3raw
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

labels = ['all countries', 'fixed set\nof countries']
colors = ['#e41a1c', 'grey']
colors2 = ['blue', 'grey']

fig, ax = plt.subplots(nrows=2, ncols=1, sharex='col', sharey='row')
axs = fig.axes
# title
ax[0].set_title(
    'Refugees as a percentage of origin country population', loc='left')
ax[0].plot(data.index, data['p_origin'], color='#e41a1c', linestyle='solid')
ax[0].plot(data.index, data['p_origin_fixed'],
           color='grey', linestyle='dotted')

ax[1].set_title(
    'Refugees as a percentage of residence country population', loc='left')
ax[1].plot(data.index, data['p_residence'], color='blue', linestyle='dashed')
ax[1].plot(data.index, data['p_residence_fixed'],
           color='grey', linestyle='dotted')

# annotations/legend
maxyear = data.index.max()
for (c, kleur, lab) in zip(['p_origin', 'p_origin_fixed'], colors, labels):
    ax[0].text(x=maxyear + 1, y=data.at[maxyear, c], s=lab, color=kleur)
for (c, kleur, lab) in zip(['p_residence', 'p_residence_fixed'], colors2, labels):
    ax[1].text(x=maxyear + 1, y=data.at[maxyear, c], s=lab, color=kleur)


for ax in axs:
    ax.yaxis.set_major_formatter(tick.PercentFormatter(xmax=100))


# range in years.
xranger = list(range(1980, 2015, 5))
xranger[0] = 1980
xranger = xranger+[2016]

for ax in fig.axes:
    ax.grid(which='major', axis='y', linestyle=':')
    ax.set_xlim([1980, 2016])
    ax.set_xticks(xranger)
sns.despine()

sns.despine()
plt.subplots_adjust(hspace=0.3)
fig.suptitle(
    'Refugees relative to origin and residence country population (%):\n1980-2018', y=1.05, x=0.5)
# footnotes
plt.figtext(x=0, y=0, s="Source: UNHCR population statistics database, authors’ calculations.",
            fontsize='small', fontstyle='italic', fontweight='light', color='gray')

# save
plt.savefig(graphs/"Fig3_Ref_relative_origin_residence.svg",
            transparent=True, bbox_inches='tight', pad_inches=0)

plt.show()
