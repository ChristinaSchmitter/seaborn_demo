#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting with Seaborn

"""

import seaborn as sns
import matplotlib.pyplot as plt


def cat_plots(data, plot_type, factor, measure, hue = None, col = None):


    plotting_colors = {'movement_type':       {'Active': (49/255,130/255,189/255), 'Passive':  (158/255,202/255,225/255)},
                       'adaptation_delay':    {'0 ms':   (253/255,174/255,97/255), '150 ms':   (215/255,25/255,28/255)},
                       'test_modality':       {'Visual': (223/255,194/255,125/255),'Auditory': (1/255,133/255,113/255)},
                       'adaptation_modality': {'Visual': (223/255,194/255,125/255),'Auditory': (1/255,133/255,113/255)}}
    
    labels = {'thresholds':          'Threshold [ms]',
              'slopes':              'Slope',
              'widths':              'Width [ms]',
              'movement_type':       'Movement type',
              'adaptation_delay':    'Adaptation delay',
              'test_modality':       'Test modality',
              'adaptation_modality': 'Adaptation modality'}

    
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale = 1.75)
    
    if hue is None: color = plotting_colors[factor]
    else:           color = plotting_colors[hue]

    plot = sns.catplot(x = factor, 
                       y = measure, 
                       hue = hue,
                       col = col,
                       data = data, 
                       kind = plot_type, 
                       height = 6,
                       palette = color,
                       sharey = True)
    
    if hue is not None: plot._legend.set_title(labels[hue])
    
    if col is not None:
        plot.set_titles("{col_name}", fontsize = 15) 
        plot.axes.flat[0].set_ylabel(labels[measure])
        for axis in range(2): plot.axes.flat[axis].set_xlabel(labels[factor])
    else:
        plt.ylabel(labels[measure])
        plt.xlabel(labels[factor])
    
    plt.show()
 
    
 
    
def plot_types(plot_type, data):
    
    if plot_type == 'estimate':
        
        fig, axes = plt.subplots(1, 2, figsize = (15, 5), sharey = False)
        
        sns.barplot(ax = axes[0], data = data, x = 'movement_type', y = 'thresholds', palette = 'crest')
        axes[0].set_title('Barplot')
        
        sns.pointplot(ax = axes[1], data = data, x = 'movement_type', y = 'thresholds')
        axes[1].set_title('Pointplot')
        
        for axis in range(2): axes[axis].set_xlabel('Movement type')
        for axis in range(2): axes[axis].set_ylabel('Threshold [ms]') 
        plt.tight_layout()    
        plt.show()  
        
        
    elif plot_type == 'distribution':
        
        fig, axes = plt.subplots(1, 3, figsize = (15, 5), sharey = False)
        
        sns.boxplot(ax = axes[0], data = data, x = 'movement_type', y = 'thresholds', palette = 'crest')
        axes[0].set_title('Boxplot')
        
        sns.boxenplot(ax = axes[1], data = data, x = 'movement_type', y = 'thresholds', palette = 'crest')
        axes[1].set_title('Boxenplot')
        
        sns.violinplot(ax = axes[2], data = data, x = 'movement_type', y = 'thresholds', palette = 'crest')
        axes[2].set_title('Violinplot')
        
        for axis in range(3): axes[axis].set_xlabel('Movement type')
        for axis in range(3): axes[axis].set_ylabel('Threshold [ms]')
        plt.tight_layout()
        plt.show()  
        
        
    elif plot_type == 'scatter':
        
        fig, axes = plt.subplots(1, 2, figsize = (15, 5), sharey = False)
        
        sns.stripplot(ax = axes[0], data = data, x = 'movement_type', y = 'thresholds', palette = 'crest')
        axes[0].set_title('Stripplot')
        
        sns.swarmplot(ax = axes[1], data = data, x = 'movement_type', y = 'thresholds', palette = 'crest')
        axes[1].set_title('Swarmplot')
        
        for axis in range(2): axes[axis].set_xlabel('Movement type')
        for axis in range(2): axes[axis].set_ylabel('Threshold [ms]')
        plt.tight_layout()
        plt.show()              
    
    
    

def plot_dist(data, measure):    
    
    labels = {'movement_durations': 'Button press durations [ms]',
              'movement_latencies': 'Button press latencies [ms]'}
    
    plot = sns.FacetGrid(data, row = 'participant', hue = 'participant', aspect = 10, height = 1.0, palette = 'crest')
    
    # add the densities kdeplots for each participant
    plot.map(sns.kdeplot, measure, bw_adjust = 1, clip_on = False, fill = True, alpha = 1, linewidth = 1.5)
        
    # add a horizontal line for each plot
    plot.map(plt.axhline, y = 0, lw = 2, clip_on = False)

    for i, ax in enumerate(plot.axes.flat):
        ax.text(data[measure].min() - 200, 0.002, 'P' + str(i+1), fontweight = 'bold', fontsize = 15, color = ax.lines[-1].get_color())
    
    # remove axes titles, yticks and spines
    plot.set_titles("")
    plot.set(yticks=[])
    plot.despine(bottom = True, left = True)
       
    plt.xlabel(labels[measure], fontsize = 15, fontweight = 'bold')
    plt.xticks(fontsize = 15, fontweight = 'bold')
    
    plt.show()

    
    
    
