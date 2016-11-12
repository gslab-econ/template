import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('build/data/data.txt', delimiter = '|', header = 0)
plt.hist(data['count'])
fig = plt.gcf()
fig.savefig('output/analysis/plot.eps')

open('output/analysis/table.txt', 'wb').write('<tab:table>\n')
data.groupby('group').sum().to_csv('output/analysis/table.txt', mode = 'a', sep = '\t', header = False)
