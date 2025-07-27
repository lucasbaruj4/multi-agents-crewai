"""
Company Profile Package
======================

This package contains all company profile management components including
the CompanyProfile class, ExecutiveQuestionnaire, and related utilities
for personalized market research.
"""

from .company_profile import CompanyProfile, create_sample_profile, get_profile_filepath
from .executive_questionnaire import ExecutiveQuestionnaire, run_questionnaire

__all__ = [
    'CompanyProfile',
    'create_sample_profile', 
    'get_profile_filepath',
    'ExecutiveQuestionnaire',
    'run_questionnaire'
] 