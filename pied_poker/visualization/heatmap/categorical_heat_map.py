import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class CategoricalHeatmap:
    @staticmethod
    def visualize(df: pd.DataFrame, title: str = None, color: str = 'seagreen'):
        """
        Allows you to visualize a dataframe as a heatmap, using the index as the Y-axis variables and the columns as
        the x-axis. Every value inside the dataframe must be numeric.

        For example, maybe you are trying to visualize the probability of winning for different starting hands for
        different table sizes. The dataframe might look something like this:

                        2 Players       3 Players       4 Players
        (starting_hand)
            AA          0.8             0.7             0.6
            66          0.5             0.4             0.3
            22          0.4             0.3             0.2

        :param df: The dataframe to visualize, all values must be numeric and it must have column names and an index.
        :type df: pd.DataFrame
        :param title: The title of the graph
        :type title: str
        :param color: The Seaborn color of the heatmap, default is green
        :type color: str
        :return: None
        :rtype: None
        """
        # from https://stackoverflow.com/questions/36227475/heatmap-like-plot-but-for-categorical-variables-in-seaborn
        values = df.values.ravel()
        n = len(values)

        # discrete colormap (n samples from a given cmap)
        cmap = sns.light_palette(color, as_cmap=True)
        ax = sns.heatmap(df, cmap=cmap)

        # modify colorbar:
        colorbar = ax.collections[0].colorbar
        num_ticks = 10
        values_safe = [v for v in values if not pd.isna(v)]
        colorbar_values = [round(v, 2) for v in np.linspace(min(values_safe), max(values_safe), num_ticks)]

        colorbar.set_ticks(colorbar_values)
        colorbar.set_ticklabels(colorbar_values)
        plt.title(title)
        plt.show()