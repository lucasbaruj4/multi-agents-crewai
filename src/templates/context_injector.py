"""
Context Injector Module
======================

Smart template system for injecting company-specific context into agent definitions
and task descriptions while maintaining token optimization and API usage efficiency.
"""

import re
from typing import Dict, Any, List, Optional
from string import Template

from src.company_profile import CompanyProfile


class ContextInjector:
    """
    Smart context injection system for company-specific personalization.
    
    This class handles the intelligent injection of company information into
    agent definitions and task descriptions while maintaining strict token
    budgets and API usage optimization.
    """
    
    def __init__(self, company_profile: CompanyProfile):
        """
        Initialize the context injector with a company profile.
        
        Args:
            company_profile: CompanyProfile instance with company information
        """
        self.profile = company_profile
        self.context_vars = self._build_context_variables()
    
    def _build_context_variables(self) -> Dict[str, str]:
        """
        Build context variables from company profile for template injection.
        
        Returns:
            Dictionary of context variables for template substitution
        """
        return {
            # Basic company info
            'company_name': self.profile.company_name,
            'industry': self.profile.industry,
            'company_description': self.profile.company_description,
            
            # Business context
            'target_customers': ', '.join(self.profile.target_customers),
            'products_services': ', '.join(self.profile.products_services),
            'business_model': self.profile.business_model,
            
            # Competitive intelligence
            'main_competitors': ', '.join(self.profile.main_competitors),
            'competitive_advantages': ', '.join(self.profile.competitive_advantages),
            'market_position': self.profile.market_position,
            
            # Strategic priorities
            'current_challenges': ', '.join(self.profile.current_challenges),
            'strategic_goals': ', '.join(self.profile.strategic_goals),
            'research_focus_areas': ', '.join(self.profile.research_focus_areas),
            
            # Compact versions for token optimization
            'compact_context': self.profile.get_compact_context(),
            'context_summary': self.profile.get_context_summary(),
            
            # Industry-specific focus
            'industry_focus': self._get_industry_focus(),
            'competitive_focus': self._get_competitive_focus(),
            'strategic_focus': self._get_strategic_focus()
        }
    
    def _get_industry_focus(self) -> str:
        """Get industry-specific focus areas."""
        industry = self.profile.industry.lower()
        
        if 'tech' in industry or 'software' in industry:
            return "technology trends, innovation, digital transformation"
        elif 'health' in industry:
            return "healthcare regulations, patient outcomes, medical technology"
        elif 'finance' in industry:
            return "financial regulations, fintech innovation, risk management"
        elif 'retail' in industry:
            return "e-commerce trends, customer experience, supply chain"
        else:
            return "industry trends, market dynamics, competitive landscape"
    
    def _get_competitive_focus(self) -> str:
        """Get competitive intelligence focus areas."""
        competitors = ', '.join(self.profile.main_competitors[:3])
        advantages = ', '.join(self.profile.competitive_advantages[:2])
        return f"competitors ({competitors}), advantages ({advantages})"
    
    def _get_strategic_focus(self) -> str:
        """Get strategic priorities focus areas."""
        goals = ', '.join(self.profile.strategic_goals[:2])
        challenges = ', '.join(self.profile.current_challenges[:2])
        return f"goals ({goals}), challenges ({challenges})"
    
    def inject_context(self, template: str, token_budget: int = 150) -> str:
        """
        Inject company context into a template while respecting token budget.
        
        Args:
            template: Template string with placeholders like ${company_name}
            token_budget: Maximum tokens to add (default: 150)
            
        Returns:
            Template with injected context, optimized for token usage
        """
        # First, try full context injection
        try:
            result = Template(template).safe_substitute(self.context_vars)
            
            # Estimate token usage (rough approximation: 1 token ≈ 4 characters)
            estimated_tokens = len(result) // 4
            
            if estimated_tokens <= token_budget:
                return result
            
        except Exception:
            pass
        
        # If token budget exceeded, use compact injection
        return self._inject_compact_context(template, token_budget)
    
    def _inject_compact_context(self, template: str, token_budget: int) -> str:
        """
        Inject compact context to stay within token budget.
        
        Args:
            template: Template string
            token_budget: Maximum tokens to add
            
        Returns:
            Template with compact context injection
        """
        # Create compact context variables
        compact_vars = {
            'company_name': self.profile.company_name,
            'industry': self.profile.industry,
            'compact_context': self.profile.get_compact_context(),
            'target_customers': ', '.join(self.profile.target_customers[:2]),
            'main_competitors': ', '.join(self.profile.main_competitors[:2]),
            'strategic_goals': ', '.join(self.profile.strategic_goals[:1]),
            'research_focus': ', '.join(self.profile.research_focus_areas[:2])
        }
        
        # Replace complex placeholders with compact versions
        template = self._replace_complex_placeholders(template, compact_vars)
        
        # Apply compact substitution
        try:
            result = Template(template).safe_substitute(compact_vars)
            return result
        except Exception:
            # Fallback: return template with minimal substitution
            return template.replace('${company_name}', self.profile.company_name)
    
    def _replace_complex_placeholders(self, template: str, compact_vars: Dict[str, str]) -> str:
        """
        Replace complex placeholders with compact versions.
        
        Args:
            template: Template string
            compact_vars: Compact context variables
            
        Returns:
            Template with simplified placeholders
        """
        # Replace complex placeholders with simpler ones
        replacements = {
            '${context_summary}': '${compact_context}',
            '${target_customers}': '${target_customers}',
            '${products_services}': '${company_name} products',
            '${main_competitors}': '${main_competitors}',
            '${competitive_advantages}': '${company_name} advantages',
            '${current_challenges}': '${company_name} challenges',
            '${strategic_goals}': '${strategic_goals}',
            '${research_focus_areas}': '${research_focus}'
        }
        
        for old, new in replacements.items():
            template = template.replace(old, new)
        
        return template
    
    def get_agent_context(self, agent_type: str) -> str:
        """
        Get company-specific context for agent definitions.
        
        Args:
            agent_type: Type of agent ('archivist', 'shadow', 'nexus')
            
        Returns:
            Company-specific context string for agent
        """
        contexts = {
            'archivist': f"Specialized in {self.profile.industry} market research for {self.profile.company_name}. Focus on {', '.join(self.profile.research_focus_areas[:2])}.",
            'shadow': f"Expert in competitive analysis for {self.profile.company_name} against {', '.join(self.profile.main_competitors[:2])}. Understands {self.profile.market_position}.",
            'nexus': f"Strategic advisor for {self.profile.company_name} with focus on {', '.join(self.profile.strategic_goals[:2])}. Addresses challenges: {', '.join(self.profile.current_challenges[:2])}."
        }
        
        return contexts.get(agent_type, f"Expert in {self.profile.industry} for {self.profile.company_name}.")
    
    def get_task_context(self, task_type: str) -> str:
        """
        Get company-specific context for task descriptions.
        
        Args:
            task_type: Type of task ('market_segments', 'research', 'competitor', 'summary')
            
        Returns:
            Company-specific context string for task
        """
        contexts = {
            'market_segments': f"Focus on {self.profile.industry} segments relevant to {self.profile.company_name} and {', '.join(self.profile.target_customers[:2])}.",
            'research': f"Research sources for {self.profile.company_name} in {self.profile.industry}, focusing on {', '.join(self.profile.research_focus_areas[:2])}.",
            'competitor': f"Analyze {', '.join(self.profile.main_competitors[:3])} for {self.profile.company_name} competitive positioning.",
            'summary': f"Executive summary for {self.profile.company_name} focusing on {', '.join(self.profile.strategic_goals[:2])} and {', '.join(self.profile.research_focus_areas[:2])}."
        }
        
        return contexts.get(task_type, f"Analysis for {self.profile.company_name} in {self.profile.industry}.")
    
    def validate_template(self, template: str) -> List[str]:
        """
        Validate template for proper placeholder usage.
        
        Args:
            template: Template string to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check for valid placeholders
        valid_placeholders = set(self.context_vars.keys())
        found_placeholders = re.findall(r'\$\{(\w+)\}', template)
        
        for placeholder in found_placeholders:
            if placeholder not in valid_placeholders:
                errors.append(f"Unknown placeholder: ${{{placeholder}}}")
        
        # Check for balanced braces
        if template.count('${') != template.count('}'):
            errors.append("Unbalanced placeholder braces")
        
        return errors
    
    def get_token_estimate(self, template: str) -> int:
        """
        Estimate token usage for a template after context injection.
        
        Args:
            template: Template string
            
        Returns:
            Estimated token count
        """
        try:
            result = Template(template).safe_substitute(self.context_vars)
            # Rough approximation: 1 token ≈ 4 characters
            return len(result) // 4
        except Exception:
            return len(template) // 4


def create_context_injector(company_profile: CompanyProfile) -> ContextInjector:
    """
    Convenience function to create a ContextInjector.
    
    Args:
        company_profile: CompanyProfile instance
        
    Returns:
        ContextInjector instance
    """
    return ContextInjector(company_profile)


def inject_company_context(template: str, company_profile: CompanyProfile, token_budget: int = 150) -> str:
    """
    Convenience function to inject company context into a template.
    
    Args:
        template: Template string with placeholders
        company_profile: CompanyProfile instance
        token_budget: Maximum tokens to add
        
    Returns:
        Template with injected company context
    """
    injector = ContextInjector(company_profile)
    return injector.inject_context(template, token_budget) 