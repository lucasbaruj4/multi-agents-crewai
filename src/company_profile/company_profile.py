"""
Company Profile Configuration Module
===================================

Defines the CompanyProfile class for storing and managing company-specific information
that will be injected into agent definitions and task descriptions for personalized
market research analysis.
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class CompanyProfile:
    """
    Company profile data structure for personalized market research.
    
    This class stores all company-specific information that will be injected
    into agent definitions and task descriptions to make market research
    highly targeted and relevant to the specific company.
    """
    
    # Basic Company Information
    company_name: str
    industry: str
    company_description: str
    
    # Business Context
    target_customers: List[str]
    products_services: List[str]
    business_model: str
    
    # Competitive Intelligence
    main_competitors: List[str]
    competitive_advantages: List[str]
    market_position: str
    
    # Strategic Priorities
    current_challenges: List[str]
    strategic_goals: List[str]
    research_focus_areas: List[str]
    
    # Metadata
    created_date: Optional[str] = None
    last_updated: Optional[str] = None
    
    def __post_init__(self):
        """Validate and set default values after initialization."""
        self._validate_required_fields()
        self._set_defaults()
    
    def _validate_required_fields(self):
        """Validate that all required fields are provided."""
        required_fields = [
            'company_name', 'industry', 'company_description',
            'target_customers', 'products_services', 'business_model',
            'main_competitors', 'competitive_advantages', 'market_position',
            'current_challenges', 'strategic_goals', 'research_focus_areas'
        ]
        
        for field in required_fields:
            value = getattr(self, field)
            if not value or (isinstance(value, list) and len(value) == 0):
                raise ValueError(f"Field '{field}' is required and cannot be empty")
    
    def _set_defaults(self):
        """Set default values for optional fields."""
        from datetime import datetime
        
        if not self.created_date:
            self.created_date = datetime.now().isoformat()
        if not self.last_updated:
            self.last_updated = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convert profile to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompanyProfile':
        """Create CompanyProfile from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CompanyProfile':
        """Create CompanyProfile from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save(self, filepath: Optional[str] = None) -> str:
        """
        Save profile to JSON file.
        
        Args:
            filepath: Optional custom filepath. If None, uses default location.
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filepath = self._get_default_filepath()
        
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Update last_updated timestamp
        from datetime import datetime
        self.last_updated = datetime.now().isoformat()
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
        
        return filepath
    
    @classmethod
    def load(cls, filepath: Optional[str] = None) -> 'CompanyProfile':
        """
        Load profile from JSON file.
        
        Args:
            filepath: Optional custom filepath. If None, uses default location.
            
        Returns:
            Loaded CompanyProfile instance
            
        Raises:
            FileNotFoundError: If profile file doesn't exist
            ValueError: If profile data is invalid
        """
        if filepath is None:
            filepath = cls._get_default_filepath()
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Company profile not found at: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            json_str = f.read()
        
        return cls.from_json(json_str)
    
    @classmethod
    def exists(cls, filepath: Optional[str] = None) -> bool:
        """Check if a company profile exists."""
        if filepath is None:
            filepath = cls._get_default_filepath()
        return os.path.exists(filepath)
    
    @classmethod
    def _get_default_filepath(cls) -> str:
        """Get default filepath for company profile."""
        return os.path.join('config', 'company_profile.json')
    
    def get_context_summary(self) -> str:
        """
        Get a concise summary of company context for injection into prompts.
        
        Returns:
            Formatted string with key company information
        """
        summary_parts = [
            f"Company: {self.company_name}",
            f"Industry: {self.industry}",
            f"Description: {self.company_description}",
            f"Target Customers: {', '.join(self.target_customers)}",
            f"Products/Services: {', '.join(self.products_services)}",
            f"Business Model: {self.business_model}",
            f"Main Competitors: {', '.join(self.main_competitors)}",
            f"Competitive Advantages: {', '.join(self.competitive_advantages)}",
            f"Market Position: {self.market_position}",
            f"Current Challenges: {', '.join(self.current_challenges)}",
            f"Strategic Goals: {', '.join(self.strategic_goals)}",
            f"Research Focus: {', '.join(self.research_focus_areas)}"
        ]
        
        return " | ".join(summary_parts)
    
    def get_compact_context(self) -> str:
        """
        Get a compact version of company context for token optimization.
        
        Returns:
            Compact string with essential company information
        """
        return f"{self.company_name} ({self.industry}): {self.company_description[:100]}... | Customers: {', '.join(self.target_customers[:3])} | Competitors: {', '.join(self.main_competitors[:3])} | Goals: {', '.join(self.strategic_goals[:2])}"
    
    def update(self, **kwargs) -> None:
        """
        Update profile fields and save.
        
        Args:
            **kwargs: Field names and new values to update
        """
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
            else:
                raise ValueError(f"Unknown field: {field}")
        
        # Update timestamp
        from datetime import datetime
        self.last_updated = datetime.now().isoformat()
    
    def validate(self) -> List[str]:
        """
        Validate profile data and return list of validation errors.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Check required fields
        if not self.company_name.strip():
            errors.append("Company name cannot be empty")
        
        if not self.industry.strip():
            errors.append("Industry cannot be empty")
        
        if len(self.company_description.strip()) < 10:
            errors.append("Company description must be at least 10 characters")
        
        # Check list fields have content
        list_fields = [
            'target_customers', 'products_services', 'main_competitors',
            'competitive_advantages', 'current_challenges', 'strategic_goals',
            'research_focus_areas'
        ]
        
        for field in list_fields:
            value = getattr(self, field)
            if not value or not all(item.strip() for item in value):
                errors.append(f"{field.replace('_', ' ').title()} must contain valid entries")
        
        return errors


def create_sample_profile() -> CompanyProfile:
    """
    Create a sample company profile for testing and demonstration.
    
    Returns:
        Sample CompanyProfile instance
    """
    return CompanyProfile(
        company_name="TechFlow Solutions",
        industry="Enterprise Software",
        company_description="A B2B SaaS company specializing in workflow automation and process optimization for mid-market enterprises.",
        target_customers=["Mid-market enterprises", "Operations managers", "Process improvement teams"],
        products_services=["Workflow automation platform", "Process analytics dashboard", "Integration APIs"],
        business_model="SaaS subscription with tiered pricing",
        main_competitors=["Zapier", "Microsoft Power Automate", "UiPath"],
        competitive_advantages=["Enterprise-grade security", "Custom integration capabilities", "Advanced analytics"],
        market_position="Emerging challenger in workflow automation",
        current_challenges=["Market penetration", "Brand recognition", "Sales cycle length"],
        strategic_goals=["Expand market share", "Develop enterprise partnerships", "Launch AI-powered features"],
        research_focus_areas=["Competitive positioning", "Market expansion opportunities", "Product differentiation"]
    )


def get_profile_filepath() -> str:
    """Get the standard filepath for company profile."""
    return CompanyProfile._get_default_filepath() 