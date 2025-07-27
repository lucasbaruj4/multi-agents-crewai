"""
Templates Package
================

This package contains template management and context injection components
for personalizing agent definitions and task descriptions.
"""

from .context_injector import ContextInjector, create_context_injector, inject_company_context

__all__ = ['ContextInjector', 'create_context_injector', 'inject_company_context'] 