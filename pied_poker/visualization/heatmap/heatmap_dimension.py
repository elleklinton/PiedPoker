from typing import List

from pied_poker.visualization.heatmap.heatmap_dimension_value import HeatmapDimensionValue


class HeatmapDimension:
    def __init__(self, axis_values: List[HeatmapDimensionValue], axis_name: str):
        assert type(axis_values) == type([]), f'Error: expected axis_values to be type List ' \
                                                 f'but got {type(axis_values)}.'
        self.axis_values = axis_values
        self.axis_name = axis_name

    @property
    def axis_labels(self):
        return [c.label for c in self.axis_values]

    def __str__(self):
        return str([d for d in self.axis_values])

    def __repr__(self):
        return str(self)