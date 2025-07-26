"""
Tasks Package
============

Market analysis tasks and workflows for the multi-agent research system.
"""

from .market_analysis_tasks import (
    identify_key_market_segments,
    collect_reports_news,
    profile_competitor,
    analyze_comp_markt_position,
    identify_trends,
    identify_reg_ethic_shift,
    compile_all
)

__all__ = [
    'identify_key_market_segments',
    'collect_reports_news', 
    'profile_competitor',
    'analyze_comp_markt_position',
    'identify_trends',
    'identify_reg_ethic_shift',
    'compile_all'
] 