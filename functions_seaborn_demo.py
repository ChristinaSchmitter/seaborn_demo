#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting with Seaborn

"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
import pandas as pd
from statannot import add_stat_annotation



def plot_sem(plot, data, x, y, hue = None, col = None):
    
    if hue is None:
        data_avg = (data.groupby([x], sort = False)[y].agg([np.mean, scipy.stats.sem]).reset_index())
    
        for i, bar in enumerate(plot.ax.patches):    
            cond   = data_avg[x].unique()[i]    
            sem    = data_avg['sem'][data_avg[x] == cond].values
            x_pos  = bar.get_x()
            width  = bar.get_width()
            height = bar.get_height()
    
            plt.errorbar(x = x_pos + width/2, y = height, yerr = sem, color = 'black', elinewidth = 2)
                      
    elif hue is not None:
        
        if col is None:
            data_avg = (data.groupby([x, hue], sort = False)[y].agg([np.mean, scipy.stats.sem]).reset_index()) 
        elif col is not None:
            data_avg = (data.groupby([col, x, hue], sort = False)[y].agg([np.mean, scipy.stats.sem]).reset_index())   
            
        conds = [(x_i, hue_i) for hue_i in data_avg[hue].unique() for x_i in data_avg[x].unique()]
               
        for ax in plot.axes.ravel():
            for i, bar in enumerate(ax.patches):    
                
                if col is None:
                    sem  = data_avg['sem'][(data_avg[x]   == conds[i][0]) & \
                                           (data_avg[hue] == conds[i][1])].values
                elif col is not None:               
                    sem  = data_avg['sem'][(data_avg[col] == ax.title.get_text()) & \
                                           (data_avg[x]   == conds[i][0]) & \
                                           (data_avg[hue] == conds[i][1])].values
                x_pos  = bar.get_x()
                width  = bar.get_width()
                height = bar.get_height()
                
                ax.errorbar(x = x_pos + width/2, y = height, yerr = sem, color = 'black', elinewidth = 2)
        
              
                

def cat_plots(data, plot_type, x, y, plotting_colors, labels, hue = None, col = None):
    
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale = 1.75)
    
    if hue is None: color = plotting_colors[x]
    else:           color = plotting_colors[hue]

    plot = sns.catplot(x = x, 
                       y = y, 
                       hue = hue,
                       col = col,
                       data = data, 
                       kind = plot_type, 
                       height = 6,
                       palette = color,
                       sharey = True)
    
    if hue is not None: plot._legend.set_title(labels[y])
    
    if col is not None:
        plot.set_titles("{col_name}", fontsize = 15) 
        plot.axes.flat[0].set_ylabel(labels[y])
        for axis in range(2): plot.axes.flat[axis].set_xlabel(labels[x])
    else:
        plt.ylabel(labels[y])
        plt.xlabel(labels[x])
    
    plt.show()
     
 
    

def statistical_annotation(plot, kind, data, comp_pairs, pvalues, x, y, hue = None, col = None):
    
    """    
    comp_pairs, pvalues: 
        Examples shape of input
        1 categorical variable:
            comp_pairs = [[(x_i),(x_j)]]
            pvalues    = [[pval]]
            
        2 categorical variables:
            comp_pairs = [[(x_i,hue_i),(x_i,hue_j)],
                          [(x_j,hue_i),(x_j,hue_j)]]
            pvalues    = [[pval_pair1], [pval_pair2]] 
        
        3 categorical variables:
            comp_pairs = [[(col_i,x_i,hue_i),(col_i,x_i,hue_j)],
                          [(col_j,x_i,hue_i),(col_i,x_i,hue_j)]]
            pvalues    = [[pval_pair1], [pval_pair2]]
    """
    
    if hue is None and col is None:   
        if kind == 'bar':
            data_avg = (data.groupby([x], sort = False).mean().reset_index()) 
        elif kind in ['box', 'boxen', 'violin', 'strip', 'swarm']:
            raise NotImplementedError()

        for ax in plot.axes.ravel():
            for i, comp in enumerate(comp_pairs):                      
                add_stat_annotation(ax, data = data_avg, x = x, y = y, hue = hue,
                                    box_pairs = [comp], 
                                    perform_stat_test = False, 
                                    pvalues = pvalues[i],
                                    text_format = 'star', 
                                    loc = 'inside', 
                                    line_height = 0, 
                                    line_offset_to_box = 0.1)
       
    if hue is not None and col is None:  
        if kind == 'bar':
            data_avg = (data.groupby([x, hue], sort = False).mean().reset_index()) 
        elif kind in ['box', 'boxen', 'violin', 'strip', 'swarm']:
            raise NotImplementedError('Function is currently only working for plots of kind = bar')            

        for ax in plot.axes.ravel():            
            for i, comp in enumerate(comp_pairs):                          
                add_stat_annotation(ax, data = data_avg, x = x, y = y, hue = hue,
                                    box_pairs = [comp], 
                                    perform_stat_test = False, 
                                    pvalues = pvalues[i],
                                    text_format = 'star', 
                                    loc = 'inside', 
                                    line_height = 0, 
                                    line_offset_to_box = 0.1)

    if col is not None:
        for ax in plot.axes.ravel():
            
            for i, comp in enumerate(comp_pairs):                     
                if ax.title.get_text() in comp[0]:                    
                    data_avg = (data.groupby([col, x, hue], sort = False).mean().reset_index()) 
                    data_avg = data_avg[data_avg[col] == ax.title.get_text()]
                    
                    cmp = [[tuple([item for item in cond if item != ax.title.get_text()]) for cond in comp]]
                                        
                    add_stat_annotation(ax, data = data_avg, x = x, y = y, hue = hue,
                                        box_pairs = cmp, 
                                        perform_stat_test = False, 
                                        pvalues = pvalues[i],
                                        text_format = 'star', 
                                        loc = 'inside', 
                                        line_height = 0, 
                                        line_offset_to_box = 0.1)

    



if __name__ == "__main__":   
    
    
    group_stats = pd.read_excel('group_stats.xlsx')
    
    
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
    



    cat_plots(data = group_stats, 
              plot_type = 'violin', 
              x = 'movement_type', 
              y = 'thresholds', 
              plotting_colors = plotting_colors, 
              labels = labels, 
              hue = 'adaptation_delay')
             
      
