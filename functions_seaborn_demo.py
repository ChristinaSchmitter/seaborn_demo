#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seaborn Demo
20.01.2022

"""

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import scipy
import pandas as pd
from statannot import add_stat_annotation
from statannotations.Annotator import Annotator



def plot_sem(plot, data, x, y, hue = None, col = None):
    
    """
    Plotting error bars indicating stantard errors of the means to seaborn catplots of kind = bar
    
    Args:
        plot: seaborn catplot
        data: pandas dataframe of data used for plotting
        x:    categorical variable plotted on x-axis
        y:    dependent variable
        hue:  second categorical variable 
        col:  third categorical variable
    
    """
    
    if hue is None:
        
        if len(plot.ax.patches) == 0:
            raise NotImplementedError('plot_sem is implemented for plots of kind = bar only' )

        data_avg = (data.groupby([x], sort = False)[y].agg([np.mean, scipy.stats.sem]).reset_index())
    
        for i, bar in enumerate(plot.ax.patches):  
            
            if not isinstance(bar, patches.Rectangle):
                raise NotImplementedError('plot_sem is implemented for plots of kind = bar only' )

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
            
            if len(ax.patches) == 0:
                raise NotImplementedError('plot_sem is implemented for plots of kind = bar only' )
                                
            for i, bar in enumerate(ax.patches):
                
                if not isinstance(bar, patches.Rectangle):
                    raise NotImplementedError('plot_sem is implemented for plots of kind = bar only' )
                    
                if col is None:                    
                    sem  = data_avg['sem'][(data_avg[x]   == conds[i][0]) & \
                                           (data_avg[hue] == conds[i][1])].values
                
                elif col is not None:
                    
                    if col in ax.title.get_text() and '=' in ax.title.get_text():
                        col_lvl = ax.title.get_text()[ax.title.get_text().find('=')+2:]
                    else: 
                        col_lvl = ax.title.get_text()
                    
                    sem  = data_avg['sem'][(data_avg[col] == col_lvl) & \
                                           (data_avg[x]   == conds[i][0]) & \
                                           (data_avg[hue] == conds[i][1])].values
                        
                x_pos  = bar.get_x()
                width  = bar.get_width()
                height = bar.get_height()
                
                ax.errorbar(x = x_pos + width/2, y = height, yerr = sem, color = 'black', elinewidth = 2)
        
              
                


def cat_plots(data, plot_type, x, y, plotting_colors, labels, hue = None, col = None):
    
    """
    Creating a seaborn catplot for all possible combinations of categorical variables
    
    Args:
        data:            pandas dataframe of data used for plotting
        plot_type:       can be one of ['bar', 'box', 'boxen', 'violin', 'strip', 'swarm']
        x:               categorical variable plotted on x-axis
        y:               dependent variable
        plotting_colors: 2-level dict defining colors for each level of categorical variables
        labels:          dict defining axis labels for categorical and dependent variables 
        hue:             second categorical variable 
        col:             third categorical variable 
    
    """
    
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
    Args:
        plot: seaborn catplot
        kind: can be one of ['bar', 'box', 'boxen', 'violin', 'strip', 'swarm']
        data: pandas dataframe of data used for plotting
        x:    categorical variable plotted on x-axis
        y:    dependent variable
        hue:  second categorical variable 
        col:  third categorical variable 
    
        comp_pairs, pvalues: 
            Examples shape of input
            1 categorical variable (hue and col are None):
                comp_pairs = [[(x_i),(x_j)]]
                pvalues    = [[pval]]
                
            2 categorical variables (col is None):
                comp_pairs = [[(x_i,hue_i),(x_i,hue_j)],
                              [(x_j,hue_i),(x_j,hue_j)]]
                pvalues    = [[pval_pair1], [pval_pair2]] 
            
            3 categorical variables:
                comp_pairs = [[(col_i,x_i,hue_i),(col_i,x_i,hue_j)],
                              [(col_j,x_i,hue_i),(col_i,x_i,hue_j)]]
                pvalues    = [[pval_pair1], [pval_pair2]]
    """
    
    if isinstance(plot, sns.axisgrid.FacetGrid):
        
        if hue is None and col is None: 
            
            if kind == 'bar':
                dat = (data.groupby([x], sort = False).mean().reset_index()) 
            elif kind in ['box', 'boxen', 'violin', 'strip', 'swarm']:
                dat = data
            else: raise ValueError('plot kind must be one of [bar, box, boxen, violin, strip, swarm]')
    
            for ax in plot.axes.ravel():            
                for i, comp in enumerate(comp_pairs):                      
                    add_stat_annotation(ax, data = dat, x = x, y = y, hue = hue,
                                        box_pairs = [comp], 
                                        perform_stat_test = False, 
                                        pvalues = pvalues[i],
                                        text_format = 'star', 
                                        loc = 'inside', 
                                        line_height = 0, 
                                        line_offset_to_box = 0.1)
                       
        if hue is not None and col is None:  
            
            if kind == 'bar':
                dat = (data.groupby([x, hue], sort = False).mean().reset_index()) 
            elif kind in ['box', 'boxen', 'violin', 'strip', 'swarm']:
                dat = data   
            else: raise ValueError('plot kind must be one of [bar, box, boxen, violin, strip, swarm]')
    
            for ax in plot.axes.ravel():              
                for i, comp in enumerate(comp_pairs):                          
                    add_stat_annotation(ax, data = dat, x = x, y = y, hue = hue,
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
                    
                    if col in ax.title.get_text() and '=' in ax.title.get_text():
                        col_lvl = ax.title.get_text()[ax.title.get_text().find('=')+2:]
                    else: 
                        col_lvl = ax.title.get_text()
                     
                    if col_lvl in comp[0]:  
                        
                        if kind == 'bar':
                            dat = (data.groupby([col, x, hue], sort = False).mean().reset_index()) 
                            dat = dat[dat[col] == col_lvl]
                        elif kind in ['box', 'boxen', 'violin', 'strip', 'swarm']:
                            dat = data[data[col] == col_lvl]
                        else: raise ValueError('plot kind must be one of [bar, box, boxen, violin, strip, swarm]')
                        
                        cmp = [[tuple([item for item in cond if item != col_lvl]) for cond in comp]]
                                            
                        add_stat_annotation(ax, data = dat, x = x, y = y, hue = hue,
                                            box_pairs = cmp, 
                                            perform_stat_test = False, 
                                            pvalues = pvalues[i],
                                            text_format = 'star', 
                                            loc = 'inside', 
                                            line_height = 0, 
                                            line_offset_to_box = 0.1)
    
    
    else:
        pvals = [val[0] for val in pvalues]
        
        annotator = Annotator(ax = plot,
                              data = data,
                              pairs = comp_pairs,  
                              x = x, 
                              y = y, 
                              hue = hue, 
                              order = data[x].unique())
        annotator.configure(text_format = 'star', 
                            loc = 'inside', 
                            line_height = 0)
        annotator.set_pvalues(pvals)
        annotator.annotate()
        
        
        
        


if __name__ == "__main__":   
    
    
    group_stats = pd.read_excel('data/group_stats.xlsx')
    
    
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
    
    
