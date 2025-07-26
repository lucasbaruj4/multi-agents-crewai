"""
PDF Tools Module
===============

Custom tools for creating PDF reports for the multi-agent research system.
"""

from typing import Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from fpdf import FPDF
import os


class PDFInput(BaseModel):
    """Input schema for the PDF report creation tool"""
    report_text_file: str = Field(
        ...,
        description="""The file path to the main text content of the report
                     (e.g., 'output/report_text.md')"""
    )
    image_paths: List[str] = Field(
        ...,
        description="""A list of file paths to previously generated chart images
                     (e.g., ['output/charts/chart1.png', 'output/charts/chart2.png'])"""
    )
    output_pdf_filename: str = Field(
        ...,
        description="""The desired filename for the PDF report (e.g., 'Executive_Summary_Report.pdf')"""
    )
    title_text: str = Field(
        ...,
        description="""The title that's going to be displayed in the first page of the PDF
                     (e.g., Business Research Report for MostlyOpenAI)"""
    )


class CreatePDFReportTool(BaseTool):
    """Tool for creating professional PDF reports"""
    
    name: str = "Create PDF Report"
    description: str = (
        """Assembles a professional PDF report from a given markdown/text file and a list of image paths
        Each image will be placed on a new page after the text content.
        Requires the path to the report's text content, a list of image file paths,
        the desired output PDF filename, and a main title for the report.
        Useful for generating final, shareable executive documents"""
    )
    args_schema: Type[BaseModel] = PDFInput
    
    def _run(self, report_text_file: str, image_paths: List[str],
             output_pdf_filename: str, title_text: str) -> str:
        """
        Create a professional PDF report with text content and embedded images.
        
        Args:
            report_text_file: Path to the text content file
            image_paths: List of paths to chart images
            output_pdf_filename: Name of the output PDF file
            title_text: Title for the PDF report
            
        Returns:
            Success message with file path or error message
        """
        try:
            output_dir = "output/reports"
            os.makedirs(output_dir, exist_ok=True)
            output_pdf_path = os.path.join(output_dir, output_pdf_filename)

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Add title
            pdf.set_font("Arial", size=24)
            pdf.cell(0, 20, title_text, ln=True, align='C')
            pdf.ln(10)

            # Add text content
            pdf.set_font("Arial", size=12)
            if os.path.exists(report_text_file):
                with open(report_text_file, 'r', encoding='utf-8') as f:
                    report_content = f.read()
                    pdf.multi_cell(0, 8, txt=report_content)
                pdf.ln(10)
            else:
                pdf.multi_cell(0, 8, txt=f"Warning: Report text file not found at {report_text_file}")

            # Add images
            image_counter = 0
            for img_path in image_paths:
                if os.path.exists(img_path):
                    image_counter += 1
                    pdf.add_page()  # New page for each image
                    pdf.set_font("Arial", size=10)
                    pdf.cell(0, 10, f"Figure {image_counter}: {os.path.basename(img_path)}", ln=True, align='C')
                    pdf.ln(5)
                    
                    # Add image (centered, scaled to fit page)
                    try:
                        pdf.image(img_path, x=10, y=30, w=190)
                    except Exception as img_error:
                        pdf.multi_cell(0, 8, txt=f"Error loading image {img_path}: {img_error}")
                else:
                    print(f"Warning: Image file not found at {img_path}. Skipping.")

            pdf.output(output_pdf_path)
            return f"PDF report successfully created at: {output_pdf_path}"
        except Exception as e:
            return f"Failed to create PDF report: {e}" 