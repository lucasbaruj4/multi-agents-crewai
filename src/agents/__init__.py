"""
Agents Package
=============

CrewAI agents for the multi-agent research system:
- Archivist: Expert in finding relevant market data
- Shadow: Expert in dissecting competitor strategies
- Seer: Expert analyst in identifying critical shifts
- Nexus: Expert in concise and actionable reporting
"""

from .archivist import Archivist
from .shadow import Shadow
from .seer import Seer
from .nexus import Nexus

__all__ = ['Archivist', 'Shadow', 'Seer', 'Nexus'] 