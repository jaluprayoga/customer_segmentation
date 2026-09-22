# Fungsi untuk Visualisasi


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_pie_chart(
    data,
    title,
    labels=None,
    autopct='%1.2f%%',
    colors=None,
    explode=None,
    startangle=140,
    figsize=(6, 6),
    shadow=False
):
    """
    Fungsi visualisasi Pie Chart untuk menampilkan proporsi data.
    
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if labels is None and hasattr(data, 'index'):
        labels = data.index
        
    ax.pie(
        data,
        labels=labels,
        autopct=autopct,
        startangle=startangle,
        colors=colors,
        explode=explode,
        shadow=shadow
    )
    ax.set_title(title, fontsize=13, fontweight='bold', pad=14)
    plt.tight_layout()
    plt.show()


def plot_bar_chart(
    data=None,
    x=None,
    y=None,
    title='',
    xlabel='',
    ylabel='',
    palette='viridis',
    order=None,
    hue=None,
    add_labels=True,
    fmt=',.0f',
    figsize=(10, 5)
):
    """
    Fungsi visualisasi Bar Chart.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Menghindari warning deprecation Seaborn untuk hue tanpa legend
    hue_arg = hue if hue is not None else (x if isinstance(x, str) and data is not None else None)
    
    ax = sns.barplot(
        data=data,
        x=x,
        y=y,
        hue=hue_arg,
        palette=palette,
        order=order,
        legend=False,
        ax=ax
    )
    
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    
    if add_labels:
        for p in ax.patches:
            height = p.get_height()
            if not np.isnan(height) and height > 0:
                ax.annotate(
                    f"{height:{fmt}}",
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center',
                    va='bottom',
                    xytext=(0, 5),
                    textcoords='offset points',
                    fontsize=10
                )
                
    plt.tight_layout()
    plt.show()
    return ax

def plot_line_chart(
    x,
    y,
    title,
    xlabel,
    ylabel,
    marker_color='red',
    line_color='tab:blue',
    add_labels=False,
    fmt=',.0f' ,
    figsize=(12, 5)
):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x, y, marker='o', color=line_color, markerfacecolor=marker_color, markersize=6, linewidth=2)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.6)
    if add_labels:
        for xi, yi in zip(x, y):
            ax.annotate(f'{yi:{fmt}}', (xi, yi), textcoords='offset points', xytext=(0, 7), ha='center', fontsize=8)
    plt.tight_layout()
    plt.show()
    return ax