
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import os

def save_plot_with_timestamp(plt, title, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{title.replace(' ', '_')}_{timestamp}.png"
    print(filename)
    filepath = os.path.join(output_path, filename)

    # Save the plot as PNG
    plt.savefig(filepath)

def boxplot_labels(METRICS,LABELS,data,TITLE,output_path):

    for metric in METRICS:
        metric_values = []
        for label in LABELS:
            label_values = data[data['LABEL'] == label][metric].values
            metric_values.append(label_values)
        
        overall_median = data[metric].median()

        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111)

        bp = ax.boxplot(metric_values,patch_artist=True,widths=0.6)
        ax.axhline(y=overall_median, color='red', linestyle='--', linewidth=2, label=f"Median: {overall_median:.2f}")


        plt.setp(bp['boxes'], color='grey')
        plt.setp(bp['whiskers'], color='000')
        plt.setp(bp['caps'], color='000')
        plt.setp(bp['caps'], linewidth=0)
        plt.setp(bp['medians'], color='000')
        plt.setp(bp['medians'], linewidth=1.5)
        plt.setp(bp['fliers'], marker='.')
        plt.setp(bp['fliers'], markerfacecolor='black')
        plt.setp(bp['fliers'], alpha=1)

        ax.set_title(TITLE, fontweight='bold', fontsize=12)
        ax.set_ylabel(metric, fontweight='bold', fontsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
    
        ax.set_xticklabels(LABELS, fontdict={'fontsize': 12, 'fontweight': 'bold'})
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
        ax.set_title(f"{metric}:{TITLE}",fontdict={'fontweight': 'bold','fontsize': 14})

        # min = np.min(data)
        # max = np.max(data)
        ax.set_ylim(bottom=0, top=None)
        
        # Display the plot
        plt.tight_layout()
        save_plot_with_timestamp(plt,f"{metric}_{TITLE}",output_path)

def boxplot_experiment_comparison(data,metric,x_titles,TITLE,output_path):

    overall_median = np.median(data)

    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)

    bp = ax.boxplot(data,patch_artist=True,widths=0.6)
    ax.axhline(y=overall_median, color='red', linestyle='--', linewidth=2, label=f"Median: {overall_median:.2f}")


    plt.setp(bp['boxes'], color='grey')
    plt.setp(bp['whiskers'], color='000')
    plt.setp(bp['caps'], color='000')
    plt.setp(bp['caps'], linewidth=0)
    plt.setp(bp['medians'], color='000')
    plt.setp(bp['medians'], linewidth=1.5)
    plt.setp(bp['fliers'], marker='.')
    plt.setp(bp['fliers'], markerfacecolor='black')
    plt.setp(bp['fliers'], alpha=1)

    ax.set_title(TITLE, fontweight='bold', fontsize=12)
    ax.set_ylabel(metric, fontweight='bold', fontsize=12)
    ax.yaxis.set_tick_params(labelsize=12)

    ax.set_xticklabels(x_titles, fontdict={'fontsize': 12, 'fontweight': 'bold'})
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_title(f"{metric}:{TITLE}",fontdict={'fontweight': 'bold','fontsize': 14})

    min = 0. 
    max = 1. 
    data_max = np.max(data)
    data_min = np.min(data)
    if max < data_max:
        max = data_max 
    if min > data_min : 
        min = data_min 
    ax.set_ylim(bottom=min, top=max)
    
    # Display the plot
    plt.tight_layout()
    save_plot_with_timestamp(plt,f"{metric}_{TITLE}",output_path)
