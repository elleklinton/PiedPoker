from typing import List, Any
import pandas as pd

from pied_poker.visualization.heatmap.categorical_heat_map import CategoricalHeatmap
from pied_poker.visualization.heatmap.heatmap_dimension import HeatmapDimension


class HeatmapGenerator:
    def __init__(self, left_dimension: HeatmapDimension, bottom_dimension: HeatmapDimension):
        self.left_dimension = left_dimension
        self.bottom_dimension = bottom_dimension

    def __generate_heatmap_dataframe__(self, print_progress: bool = True):
        df = pd.DataFrame(columns=self.bottom_dimension.axis_labels)
        df[self.left_dimension.axis_name] = self.left_dimension.axis_labels
        df = df.set_index(self.left_dimension.axis_name)

        for bottom_value in self.bottom_dimension.axis_values:
            if print_progress: print(f'Calculating {bottom_value.label} probabilities')
            for left_value in self.left_dimension.axis_values:
                df.loc[[left_value.label], [bottom_value.label]] = self.probability_of(left_value, bottom_value)

        return df.astype(float)

    def visualize(self, title: str = None):
        if title is None:
            title = f'{self.left_dimension.axis_name} vs {self.bottom_dimension.axis_name}'
        df = self.__generate_heatmap_dataframe__()
        return CategoricalHeatmap.visualize(df, title)

    def probability_of(self, left_value: Any, bottom_value: Any) -> float:
        raise NotImplementedError('Error: to use this class, you need to create a supertype and override the '
                                  'probability_of function.')


