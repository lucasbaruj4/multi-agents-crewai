"""
Plot Tools Module
================

Custom tools for generating plots and visualizations for the multi-agent research system.
"""

from typing import Type, Dict, Union, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import matplotlib.pyplot as plt
import os


class PlotInput(BaseModel):
    """Input schema for the plot generation tool"""
    data: Dict[str, Union[List[str], List[float], List[int]]] = Field(
        ...,
        description="""A dictionary containing Plot data.
                    Must have 'labels' (List[str] for x-axis categories)
                    and 'values' (List[float] or List[int] for y_axis values)
                    Example: {'labels':['Jan', 'Feb'], 'values': [100,150]}"""
    )
    plot_type: str = Field(
        ...,
        description="Type of plot to generate: 'bar' or 'line'"
    )
    title: str = Field(
        ...,
        description="The title of the plot"
    )
    x_label: str = Field(
        ...,
        description="Label for the x-axis"
    )
    y_label: str = Field(
        ...,
        description="Label for the y-axis"
    )
    output_filename: str = Field(
        ...,
        description="Desired filename for the generated plot image (e.g., 'revenue_chart.png')."
    )


class GeneratePlotTool(BaseTool):
    """Tool for generating plots and visualizations"""
    
    name: str = "Generate Plot Image"
    description: str = (
        """Generates a plot (bar or line chart) from given data and saves it as a PNG
        Useful for visualizing numerical trends and comparisons within reports.
        Requires data, plot type, title, x_label, y_label, and an output filename.
        Example usage: tool.generate_plot_image(data={'labels':['A', 'B'], 'values':[10, 20], plot_type='bar', title='Sales', x_label='Category', y_label='Amount', output_filename='sales_chart.png'})"""
    )
    args_schema: Type[BaseModel] = PlotInput

    def _run(self, data: Dict[str, Union[List[str], List[float], List[int]]], plot_type: str,
             title: str, x_label: str, y_label: str, output_filename: str) -> str:
        """
        Generate a plot from the provided data and save it as a PNG file.
        
        Args:
            data: Dictionary with 'labels' and 'values' keys
            plot_type: Type of plot ('bar' or 'line')
            title: Plot title
            x_label: X-axis label
            y_label: Y-axis label
            output_filename: Name of the output file
            
        Returns:
            Success message with file path or error message
        """
        try:
            labels = data.get('labels')
            values = data.get('values')

            if not labels or not values or len(labels) != len(values):
                return "Error: Data must contain 'labels' and 'values' of equal length."

            output_dir = "output_charts"
            os.makedirs(output_dir, exist_ok=True)
            plot_path = os.path.join(output_dir, output_filename)

            plt.figure(figsize=(10, 6))

            if plot_type == 'bar':
                plt.bar(labels, values)
            elif plot_type == 'line':
                plt.plot(labels, values, marker='o')
            else:
                return f"Error: Unsupported plot_type '{plot_type}'. Must be 'bar' or 'line'."

            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()

            return f"Plot image successfully saved to: {plot_path}"
        except Exception as e:
            return f"Failed to generate plot: {e}" 