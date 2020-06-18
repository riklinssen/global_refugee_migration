import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
from funcs import reformat_large_tick_values
import matplotlib.ticker as tick

# paths
root = Path.cwd()
dta = root/"data/dta"
graphs = root/"manuscript/graphs"


glob_overview = pd.read_stata(dta/"global overview.dta")

data = glob_overview.loc[:, ['Year', 'Refugees',
                             'IDPs', 'Totaldisplaced', 'Worldpop']]
# lowercase
data.columns = [c.lower() for c in data.columns]
# make a datetime index
data['yr'] = data['year'].apply(lambda x: '1/1/' + str(x))
data['year'] = pd.to_datetime(data['yr'], infer_datetime_format=True)
data.set_index('year', inplace=True)
data.index = pd.to_datetime(data.index, format='%Y').year
# to numeric exclude missings
for c in ['idps', 'totaldisplaced']:
    data[c] = pd.to_numeric(data[c], errors='coerce')

# drop redundant
data = data.drop(columns='yr')


# in percentages
data['p_refugees'] = data['refugees']/data['worldpop']
data['p_idps'] = data['idps']/data['worldpop']
data['p_totaldisplaced'] = data['totaldisplaced']/data['worldpop']

###################PLOT#############################

# figure 1 Global displacement: 1951 - 2018 (absolute numbers, in millions)
# colormap photocopy safe
colors = ['#e41a1c', '#377eb8', '#4daf4a']
labels = ["Total displaced", "IDPs", "Refugees"]

sns.set_context('paper')
plt.style.use('seaborn-ticks')

totallist = ['totaldisplaced', 'idps', 'refugees']
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex='col')
# total displaced
ax1.plot(data.index, data['totaldisplaced'],
         color='#e41a1c', linestyle='solid')
# idps
ax1.plot(data.index, data['idps'], color='#377eb8', linestyle='dashed')
# refugees
ax1.plot(data.index, data['refugees'], color='#4daf4a', linestyle='dotted')
ax1.set_title("Absolute numbers (in millions)", loc='left')
# bootm axes
# total displaced
ax2.plot(data.index, data['p_totaldisplaced'],
         color='#e41a1c', linestyle='solid')
# idps
ax2.plot(data.index, data['p_idps'], color='#377eb8', linestyle='dashed')
# refugees
ax2.plot(data.index, data['p_refugees'], color='#4daf4a', linestyle='dotted')
ax2.set_title("Relative to the world population (%)", loc='left')


# annotations/legend
maxyear = data.index.max()
for (c, kleur, lab) in zip(['totaldisplaced', 'idps', 'refugees'], colors, labels):
    ax1.text(x=maxyear+1.5, y=data.at[maxyear, c], s=lab, color=kleur)
for (c, kleur, lab) in zip(['p_totaldisplaced', 'p_idps', 'p_refugees'], colors, labels):
    ax2.text(x=maxyear+1.5, y=data.at[maxyear, c], s="% "+lab, color=kleur)

# y-axis
ax1.yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))

ax2.set_ylim([0, 0.0126])
ax2.yaxis.set_major_formatter(tick.PercentFormatter(xmax=1))


# range in years.
xranger = list(range(1950, 2020, 10))
xranger[0] = 1951
xranger = xranger+[2018]

for ax in fig.axes:
    ax.grid(which='major', axis='y', linestyle=':')
    ax.set_xlim([1951, 2018])
    ax.set_xticks(xranger)

sns.despine()
plt.subplots_adjust(hspace=0.3)
fig.suptitle('Global displacement: 1951 - 2018', y=1.05, x=0.25)

# footnotes
plt.figtext(x=0, y=-0.1, s="Source: UNHCR population statistics database, authors’ calculations.\nData for IDPs cover 1993 to 2018",
            fontsize='small', fontstyle='italic', fontweight='light', color='gray')

# save
plt.savefig(graphs/"Fig1_global_displacment.svg",
            transparent=True, bbox_inches='tight', pad_inches=0)
# export=glob_overview.to_csv('test.csv')


################################################
