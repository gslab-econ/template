import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main(): 
    
    CONFIG =  yaml.load(open('config_global.yaml', 'rU'))
    X = pd.read_csv('%s/data.csv' % CONFIG['build']['draw_data'])
    
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    
    hist, xedges, yedges = np.histogram2d(X.x1, X.x2, bins=100, range=[[-5, 5], [-5, 5]])
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0
    dx = dy = 0.5 * np.ones_like(zpos)
    dz = hist.ravel()
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
    
    plt.savefig('%s/plot.eps' % CONFIG['build']['plot'])

main()