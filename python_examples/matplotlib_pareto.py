# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:09:47 2015

@author: dthor

Example showing how I make Pareto Plots in MatPlotLib.
"""

# ----------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import random
import itertools

# Third Party
import numpy as np
import matplotlib.pyplot as plt


def main():
    """ Displays a Pareto Plot """
    #########################
    ##### User Inputs #####
    #########################
    num_pts = 100
    categories = list("abcdef")
    limit = 1.0                         # 1: all data. 0.8: only top 80%
    random.seed(56327)


    ##############################
    ##### Generate Fake Data #####
    ##############################
    # Generate some random data. A list of labels.
    weights = [round(random.random() * 100) for _ in categories]
    weights[0] = 600        # force some more extreme cases
    weights[-1] = 400
    weighted_labels = [[x] * y for x, y in zip(categories, weights)]
    weighted_labels = list(itertools.chain(*weighted_labels))
    data = [random.choice(weighted_labels) for _ in range(num_pts)]

    # This is where most implemtations would start.
    #   `data` should look like: ['a', 'a', 'b', 'c', 'a', 'c', ... ]
    #   since this next part calculates that pareto info.
    # Convert raw data to the required form: a sorted list of counts and a
    #   sorted list of labels.
    labels, counts = np.unique(data, return_counts=True)

    # re-order in descending order
    sort_order = np.argsort(counts, kind='heapsort')[::-1]
    counts = counts[sort_order]
    categories = labels[sort_order]

    # Generate the cumulative line data
    line_data = [0.0] * len(counts)
    total_data = float(sum(counts))
    for i, d in enumerate(counts):
        # TODO: this loop seems wonky. Is there a better way?
        if i == 0:
            line_data[i] = d/total_data
        else: line_data[i] = sum(counts[:i + 1])/total_data

    # Trim the data to the limit
    #   Note that the 1st point that falls above `limit` is also displayed.
    ltcount = 0
    for _x in line_data:
        if _x < limit:
            ltcount += 1
    limit_loc = range(ltcount + 1)

    counts = [counts[i] for i in limit_loc]
    categories = [categories[i] for i in limit_loc]
    line_data = [line_data[i] for i in limit_loc]

    ########################
    ##### Create Plots #####
    ########################
    # Create the main figure
    fig = plt.figure()
    axes = fig.add_subplot(111)
    ax2 = axes.twinx()

    # Plot the Pareto
    length = len(counts)
    axes.bar(range(length),
                  counts,
                  align='center',
                  picker=10,
                  )

    # Format it
    axes.grid()
    axes.set_axisbelow(True)

    axes.set_xticks(range(length))
    axes.set_xlim(-0.5, length - 0.5)
    axes.set_xticklabels(categories)


    # Add the cumulative line data
    x_data = range(len(line_data))

    ax2.plot(x_data,
             [_x * 100 for _x in line_data],
             linestyle='--',
             color='r',
             marker='o',
             picker=5,
             )

    # Adjust the 2nd axis labels.
    #   Since the sum-total value is not likely to be one of the ticks,
    #   we make it the top-most one regardless of label closeness
    axes.set_ylim(0, total_data)
    loc = axes.get_yticks()
    newloc = [loc[i] for i in range(len(loc)) if loc[i] <= total_data]
    newloc += [total_data]
    axes.set_yticks(newloc)
    ax2.set_ylim(0, 100)

    # Format the y-ticks to be percentages
    yt = ["{:3d}%".format(int(_x)) for _x in ax2.get_yticks()]
    ax2.set_yticklabels(yt)

    # Add a limit line.
    if limit < 1.0:
        xmin, xmax = axes.get_xlim()
        ax2.axhline(limit * 100, xmin - 1, xmax - 1,
                    linestyle='--',
                    color='r',
                    )

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
