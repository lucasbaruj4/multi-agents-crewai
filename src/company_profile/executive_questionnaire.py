"""
Executive Questionnaire Module
==============================

Interactive CLI questionnaire for collecting company information from executives
in a user-friendly, non-technical manner. Designed to gather comprehensive
company profiles for personalized market research.
"""

import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .company_profile import CompanyProfile


class ExecutiveQuestionnaire:
    """
    Executive-friendly CLI questionnaire for company profile creation.
    
    Provides an interactive, conversational interface that guides executives
    through providing company information without requiring technical knowledge.
    """
    
    def __init__(self):
        """Initialize the questionnaire with section definitions."""
        self.sections = self._define_sections()
        self.current_section = 0
        self.responses = {}
        
    def _define_sections(self) -> List[Dict[str, Any]]:
        """Define the questionnaire sections and questions."""
        return [
            {
                "title": "Welcome & Basic Information",
                "description": "Let's start with some basic information about your company.",
                "questions": [
                    {
                        "key": "company_name",
                        "text": "What is your company's name?",
                        "type": "text",
                        "required": True,
                        "validation": lambda x: len(x.strip()) > 0,
                        "error_msg": "Company name cannot be empty"
                    },
                    {
                        "key": "industry",
                        "text": "What industry does your company operate in? (e.g., Technology, Healthcare, Finance)",
                        "type": "text",
                        "required": True,
                        "validation": lambda x: len(x.strip()) > 0,
                        "error_msg": "Industry cannot be empty"
                    },
                    {
                        "key": "company_description",
                        "text": "Please provide a brief description of what your company does (2-3 sentences):",
                        "type": "multiline",
                        "required": True,
                        "validation": lambda x: len(x.strip()) >= 20,
                        "error_msg": "Description must be at least 20 characters"
                    }
                ]
            },
            {
                "title": "Business Context",
                "description": "Now let's understand your business model and target customers.",
                "questions": [
                    {
                        "key": "target_customers",
                        "text": "Who are your primary target customers? (e.g., Small businesses, Enterprise clients, Individual consumers)",
                        "type": "list",
                        "required": True,
                        "min_items": 1,
                        "max_items": 5,
                        "validation": lambda x: len(x) >= 1,
                        "error_msg": "Please provide at least one target customer type"
                    },
                    {
                        "key": "products_services",
                        "text": "What are your main products or services?",
                        "type": "list",
                        "required": True,
                        "min_items": 1,
                        "max_items": 5,
                        "validation": lambda x: len(x) >= 1,
                        "error_msg": "Please provide at least one product or service"
                    },
                    {
                        "key": "business_model",
                        "text": "How does your company make money? (e.g., Subscription model, One-time sales, Freemium)",
                        "type": "text",
                        "required": True,
                        "validation": lambda x: len(x.strip()) > 0,
                        "error_msg": "Business model cannot be empty"
                    }
                ]
            },
            {
                "title": "Competitive Intelligence",
                "description": "Let's understand your competitive landscape.",
                "questions": [
                    {
                        "key": "main_competitors",
                        "text": "Who are your main competitors? (List 3-5 key competitors)",
                        "type": "list",
                        "required": True,
                        "min_items": 1,
                        "max_items": 5,
                        "validation": lambda x: len(x) >= 1,
                        "error_msg": "Please provide at least one competitor"
                    },
                    {
                        "key": "competitive_advantages",
                        "text": "What are your key competitive advantages? (e.g., Technology, Customer service, Price)",
                        "type": "list",
                        "required": True,
                        "min_items": 1,
                        "max_items": 5,
                        "validation": lambda x: len(x) >= 1,
                        "error_msg": "Please provide at least one competitive advantage"
                    },
                    {
                        "key": "market_position",
                        "text": "How would you describe your current market position? (e.g., Market leader, Challenger, Niche player)",
                        "type": "text",
                        "required": True,
                        "validation": lambda x: len(x.strip()) > 0,
                        "error_msg": "Market position cannot be empty"
                    }
                ]
            },
            {
                "title": "Strategic Priorities",
                "description": "Finally, let's understand your strategic goals and challenges.",
                "questions": [
                    {
                        "key": "current_challenges",
                        "text": "What are your biggest current challenges? (e.g., Market competition, Scaling, Customer acquisition)",
                        "type": "list",
                        "required": True,
                        "min_items": 1,
                        "max_items": 5,
                        "validation": lambda x: len(x) >= 1,
                        "error_msg": "Please provide at least one challenge"
                    },
                    {
                        "key": "strategic_goals",
                        "text": "What are your main strategic goals for the next 12-18 months?",
                        "type": "list",
                        "required": True,
                        "min_items": 1,
                        "max_items": 5,
                        "validation": lambda x: len(x) >= 1,
                        "error_msg": "Please provide at least one strategic goal"
                    },
                    {
                        "key": "research_focus_areas",
                        "text": "What specific areas would you like our market research to focus on? (e.g., Competitive analysis, Market expansion, Product development)",
                        "type": "list",
                        "required": True,
                        "min_items": 1,
                        "max_items": 5,
                        "validation": lambda x: len(x) >= 1,
                        "error_msg": "Please provide at least one research focus area"
                    }
                ]
            },
            {
                "title": "Review & Confirmation",
                "description": "Let's review your information before we save it.",
                "questions": []  # No questions, just review
            }
        ]
    
    def run(self) -> CompanyProfile:
        """
        Run the complete questionnaire and return a CompanyProfile.
        
        Returns:
            CompanyProfile instance with collected information
        """
        self._print_welcome()
        
        # Run through all sections
        for i, section in enumerate(self.sections):
            self.current_section = i
            self._run_section(section)
        
        # Create and validate profile
        profile = self._create_profile()
        self._print_success(profile)
        
        return profile
    
    def _print_welcome(self):
        """Print welcome message and instructions."""
        print("\n" + "="*60)
        print("🏢 COMPANY PROFILE QUESTIONNAIRE")
        print("="*60)
        print("\nWelcome! This questionnaire will help us understand your company")
        print("so we can provide personalized market research insights.")
        print("\nThe questionnaire has 5 sections and should take about 5-10 minutes.")
        print("You can press Ctrl+C at any time to exit.")
        print("\nLet's get started!")
        print("-"*60)
    
    def _run_section(self, section: Dict[str, Any]):
        """Run a single section of the questionnaire."""
        print(f"\n📋 SECTION {self.current_section + 1} OF {len(self.sections)}")
        print(f"📝 {section['title'].upper()}")
        print(f"💡 {section['description']}")
        print("-"*40)
        
        # Handle review section specially
        if section['title'] == "Review & Confirmation":
            self._run_review_section()
            return
        
        # Run questions in this section
        for question in section['questions']:
            self._ask_question(question)
    
    def _ask_question(self, question: Dict[str, Any]):
        """Ask a single question and collect response."""
        while True:
            try:
                print(f"\n❓ {question['text']}")
                
                if question['type'] == 'text':
                    response = self._get_text_input()
                elif question['type'] == 'multiline':
                    response = self._get_multiline_input()
                elif question['type'] == 'list':
                    response = self._get_list_input(question)
                else:
                    raise ValueError(f"Unknown question type: {question['type']}")
                
                # Validate response
                if question.get('validation'):
                    if not question['validation'](response):
                        print(f"❌ {question['error_msg']}")
                        continue
                
                # Store response
                self.responses[question['key']] = response
                break
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Questionnaire cancelled by user.")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
    
    def _get_text_input(self) -> str:
        """Get single-line text input."""
        return input("💬 ").strip()
    
    def _get_multiline_input(self) -> str:
        """Get multi-line text input."""
        print("💬 (Press Enter twice when finished):")
        lines = []
        while True:
            line = input()
            if line.strip() == "" and lines:  # Empty line after content
                break
            lines.append(line)
        return "\n".join(lines).strip()
    
    def _get_list_input(self, question: Dict[str, Any]) -> List[str]:
        """Get list input with item-by-item collection."""
        items = []
        min_items = question.get('min_items', 1)
        max_items = question.get('max_items', 5)
        
        print(f"💬 (Enter {min_items}-{max_items} items, press Enter when done):")
        
        while len(items) < max_items:
            item = input(f"   Item {len(items) + 1}: ").strip()
            
            if item == "":
                if len(items) >= min_items:
                    break
                else:
                    print(f"   ⚠️  Please provide at least {min_items} item(s)")
                    continue
            
            items.append(item)
        
        return items
    
    def _run_review_section(self):
        """Run the review and confirmation section."""
        print("\n📋 REVIEW YOUR INFORMATION")
        print("="*40)
        
        # Display all responses in a formatted way
        for key, value in self.responses.items():
            display_key = key.replace('_', ' ').title()
            if isinstance(value, list):
                display_value = ", ".join(value)
            else:
                display_value = str(value)
            
            print(f"\n🔹 {display_key}:")
            print(f"   {display_value}")
        
        # Ask for confirmation
        while True:
            print("\n❓ Does this information look correct? (yes/no/edit):")
            choice = input("💬 ").strip().lower()
            
            if choice in ['yes', 'y']:
                return
            elif choice in ['no', 'n']:
                print("\n🔄 Let's start over...")
                self.responses = {}
                self.current_section = 0
                self.run()
                return
            elif choice in ['edit', 'e']:
                self._edit_responses()
                return
            else:
                print("❌ Please enter 'yes', 'no', or 'edit'")
    
    def _edit_responses(self):
        """Allow user to edit specific responses."""
        print("\n📝 EDIT RESPONSES")
        print("="*30)
        
        # Show numbered list of responses
        response_items = list(self.responses.items())
        for i, (key, value) in enumerate(response_items, 1):
            display_key = key.replace('_', ' ').title()
            if isinstance(value, list):
                display_value = ", ".join(value)
            else:
                display_value = str(value)
            print(f"{i}. {display_key}: {display_value}")
        
        while True:
            try:
                print(f"\n❓ Enter the number of the item to edit (1-{len(response_items)}) or 'done':")
                choice = input("💬 ").strip()
                
                if choice.lower() == 'done':
                    break
                
                item_num = int(choice) - 1
                if 0 <= item_num < len(response_items):
                    key, _ = response_items[item_num]
                    self._edit_single_response(key)
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(response_items)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def _edit_single_response(self, key: str):
        """Edit a single response."""
        # Find the original question
        question = None
        for section in self.sections:
            for q in section['questions']:
                if q['key'] == key:
                    question = q
                    break
            if question:
                break
        
        if question:
            print(f"\n📝 Editing: {question['text']}")
            self._ask_question(question)
        else:
            print(f"❌ Could not find question for key: {key}")
    
    def _create_profile(self) -> CompanyProfile:
        """Create CompanyProfile from collected responses."""
        try:
            profile = CompanyProfile(**self.responses)
            return profile
        except Exception as e:
            print(f"❌ Error creating profile: {e}")
            print("🔄 Please run the questionnaire again.")
            sys.exit(1)
    
    def _print_success(self, profile: CompanyProfile):
        """Print success message and save profile."""
        print("\n" + "="*60)
        print("✅ COMPANY PROFILE CREATED SUCCESSFULLY!")
        print("="*60)
        
        # Save profile
        try:
            filepath = profile.save()
            print(f"\n💾 Profile saved to: {filepath}")
        except Exception as e:
            print(f"❌ Error saving profile: {e}")
        
        print(f"\n🏢 Company: {profile.company_name}")
        print(f"🏭 Industry: {profile.industry}")
        print(f"📊 Research Focus: {', '.join(profile.research_focus_areas)}")
        
        print("\n🎯 Your personalized market research is ready to begin!")
        print("   Run 'python main.py' to start your customized analysis.")
        print("\n" + "="*60)


def run_questionnaire() -> CompanyProfile:
    """
    Convenience function to run the questionnaire.
    
    Returns:
        CompanyProfile instance
    """
    questionnaire = ExecutiveQuestionnaire()
    return questionnaire.run()


if __name__ == "__main__":
    # Allow running the questionnaire directly
    try:
        profile = run_questionnaire()
        print(f"\n✅ Questionnaire completed! Profile created for: {profile.company_name}")
    except KeyboardInterrupt:
        print("\n\n👋 Questionnaire cancelled. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1) 