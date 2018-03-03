import yaml
import numpy as np
import matplotlib.pyplot as plt

def main():
    CONFIG =  yaml.load(open('config_global.yaml', 'rU'))
    data  = np.genfromtxt('%s/data.txt' % CONFIG['build']['prepare_data'], skip_header = 1)

    with open('%s/table.txt' % CONFIG['build']['descriptive'], 'w') as f:
        f.write('<tab:table>\n')
        f.write('%s\n%.3f\n%d\n%d' % (np.mean(data), np.std(data, ddof = 1), np.max(data), np.min(data)))

    plt.hist(data)
    plt.savefig('%s/plot.eps' % CONFIG['build']['descriptive'])

main()
