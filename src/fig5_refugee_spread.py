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

fig4raw = pd.read_excel(xls/"refugee_spread.xlsx")



data = fig4raw
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

labels = ['Global refugee spread', '\nRefugee\norigin spread', 'Refugee\ndestination spread']
colors = ['#e41a1c', '#4daf4a', '#984ea3']



fig, ax = plt.subplots(nrows=1, ncols=1, sharex='col', sharey='row')
axs = fig.axes
# title
#ax[0].set_title(
#    'Global refugee spread', loc='left')
axs[0].plot(data.index, data['global_refugee'], color=colors[0], linestyle='solid')


#ax[1].set_title(
#    'Refugee origin spread', loc='left')
axs[0].plot(data.index, data['refugee_origin'], color=colors[1], linestyle='dashed')


#ax[0].set_title(
#    'Refugee destination spread', loc='left')
axs[0].plot(data.index, data['refugee_destination'], color=colors[2], linestyle='dotted')


# annotations/legend
maxyear = data.index.max()
for (c, kleur, lab) in zip(['global_refugee', 'refugee_origin', 'refugee_destination'], colors, labels):
    axs[0].text(x=maxyear + 1, y=data.at[maxyear, c], s=lab, color=kleur)

#for (c, kleur, lab) in zip(['global_refugee', 'refugee_origin', 'refugee_destination'], colors2, labels):
#    ax[1].text(x=maxyear + 1, y=data.at[maxyear, c], s=lab, color=kleur)


for ax in axs:
    ax.set_ylim([0.75,1])
    ax.set_ylabel('Spread\n(Herfendahl-index)', fontstyle='italic', fontweight='light')


# range in years.
xranger = list(range(1980, 2016, 5))
xranger[0] = 1980
xranger = xranger+[2018]

for ax in fig.axes:
    ax.grid(which='major', axis='y', linestyle=':')
    ax.set_xlim([1980, 2018])
    ax.set_xticks(xranger)
sns.despine()

fig.suptitle(
    'Global spread of refugees: 1980 – 2018:\n1980-2018', y=1.05, x=0.5)
# footnotes
plt.figtext(x=0, y=0, s="Source: UNHCR population statistics database, authors’ calculations.",
            fontsize='small', fontstyle='italic', fontweight='light', color='gray')

# save
plt.savefig(graphs/"Fig5_ref_spread.svg",
            transparent=True, bbox_inches='tight', pad_inches=0)

plt.show()



##with broken y-axis
cols=['global_refugee', 'refugee_origin', 'refugee_destination']
linestijl=['solid', 'dashed', 'dotted']
labels = ['Global refugee spread\n', 'Refugee\norigin spread', 'Refugee destination spread']
colors = ['#e41a1c', '#4daf4a', '#984ea3']

widths=[1,1]
heigts=[0.7, 0.1]

f, (ax, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'width_ratios':[1], 'height_ratios': [0.75,0.1]})

for (c, kleur, ls) in zip(cols, colors, linestijl): 
    ax.plot(data.index, data[c], color=kleur, linestyle=ls)

#plot annotations & labels
# annotations/legend
maxyear = data.index.max()
for (c, kleur, lab) in zip(['global_refugee', 'refugee_origin', 'refugee_destination'], colors, labels):
    ax.text(x=maxyear + 1, y=data.at[maxyear, c], s=lab, color=kleur)



# range in years.
xranger = list(range(1980, 2016, 5))
xranger[0] = 1980
xranger = xranger+[2018]
ax.set_xlim([1980, 2018])
ax.set_xticks(xranger)
ax2.set_xlim([1980, 2018])
ax2.set_xticks(xranger)

# zoom-in / limit the view to different portions of the data
ax.set_ylim(.75, 1.)  # high values
ax.set_ylabel('Herfendahl-index', fontstyle='italic', fontweight='light')
ax2.set_ylim(0, 0.1)  # breakpoint

#spines
ax.spines['left'].set_visible(True)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(True)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(True)

ax.tick_params(axis='x', labeltop=False, labelbottom=False, length=0)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
#ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
d2=d*7
kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d2, 1 + d2), **kwargs)  # bottom-left diagonal


f.suptitle(
    'Global spread of refugees: 1980 – 2018', y=1.05, x=0.5)
# footnotes
plt.figtext(x=0, y=0, s="Source: UNHCR population statistics database, authors’ calculations.",
            fontsize='small', fontstyle='italic', fontweight='light', color='gray')

# save
plt.savefig(graphs/"Fig5_ref_spread_broken_y.svg",
            transparent=True, bbox_inches='tight', pad_inches=0)

plt.show()

