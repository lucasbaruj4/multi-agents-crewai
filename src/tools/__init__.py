"""
Tools Package
============

Custom tools for the multi-agent research system:
- Plot generation tools
- PDF report creation tools
- Web scraping tools
"""

from .plot_tools import GeneratePlotTool
from .pdf_tools import CreatePDFReportTool

__all__ = ['GeneratePlotTool', 'CreatePDFReportTool'] 