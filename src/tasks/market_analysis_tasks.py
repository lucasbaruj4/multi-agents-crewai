"""
Market Analysis Tasks Module
===========================

Market analysis tasks and workflows for the multi-agent research system.
"""

from crewai import Task


def create_market_analysis_tasks():
    """
    Create all market analysis tasks for the crew
    
    Returns:
        List of configured tasks
    """
    
    # Import agents here to avoid circular imports
    from ..agents import Archivist, Shadow, Seer, Nexus
    
    # Research tasks
    identify_key_market_segments = Task(
        description="Identify and list the primary market segments within the enterprise-grade LLM industry (e.g., finance, healthcare, legal, specialized customer service, R&D). For each segment, provide a brief overview of its specific LLM needs and growth potential.",
        expected_output="""A JSON object with the following structure:
        {
          "market_segments": [
            {
              "name": "string - segment name",
              "description": "string - 2-3 sentence overview",
              "llm_needs": ["string - specific LLM requirements"],
              "growth_potential": "string - growth rate and market size",
              "key_players": ["string - major companies in this segment"],
              "compliance_requirements": ["string - regulatory needs"],
              "estimated_market_size": "string - current market size estimate",
              "growth_rate": "float - annual growth rate percentage"
            }
          ],
          "summary": {
            "total_segments": "integer - number of segments identified",
            "largest_segment": "string - segment with highest market size",
            "fastest_growing": "string - segment with highest growth rate",
            "key_insights": ["string - 3-5 key insights about market segments"]
          }
        }""",
        agent=Archivist,
        output_key='key_market_segments'
    )
    
    collect_reports_news = Task(
        description="""Conduct an exhaustive search for the most recent and highly relevant industry reports, whitepapers, research papers, academic studies, and significant news articles (published within the last 4 months) pertaining to the enterprise-grade LLM market. Focus specifically on: 1. Adoption rates and success stories within the previously identified market segments. 2. Technological advancements and new model architectures relevant to enterprise deployment (e.g., efficiency, fine-tuning, security). 3. Specific use cases and implementation challenges faced by businesses within these segments. 4. Market dynamics, investment trends, and significant partnerships within the LLM ecosystem. Prioritize information from top-tier technology research firms, leading academic institutions, and highly reputable industry news sources. The goal is to gather a diverse and comprehensive collection of foundational documents.""",
        expected_output="""A JSON object with the following structure:
        {
          "research_sources": [
            {
              "title": "string - document title",
              "url": "string - source URL",
              "type": "string - report|whitepaper|research_paper|news_article|academic_study",
              "author": "string - author or organization",
              "publication_date": "string - YYYY-MM-DD format",
              "relevance_score": "float - 1-10 score of relevance",
              "key_findings": ["string - 3-5 main findings"],
              "market_segment_focus": ["string - relevant market segments"],
              "technology_focus": ["string - relevant technologies discussed"],
              "summary": "string - 2-3 sentence summary"
            }
          ],
          "categorization": {
            "by_type": {
              "reports": "integer - count",
              "whitepapers": "integer - count", 
              "research_papers": "integer - count",
              "news_articles": "integer - count",
              "academic_studies": "integer - count"
            },
            "by_segment": {
              "finance": "integer - count",
              "healthcare": "integer - count",
              "legal": "integer - count",
              "customer_service": "integer - count",
              "r_and_d": "integer - count"
            },
            "by_technology": {
              "rag": "integer - count",
              "fine_tuning": "integer - count", 
              "multimodal": "integer - count",
              "security": "integer - count",
              "efficiency": "integer - count"
            }
          },
          "quality_metrics": {
            "total_sources": "integer - total number of sources",
            "avg_relevance_score": "float - average relevance score",
            "date_range": {
              "earliest": "string - YYYY-MM-DD",
              "latest": "string - YYYY-MM-DD"
            },
            "top_sources": ["string - top 5 sources by relevance score"]
          }
        }""",
        context=[identify_key_market_segments],
        agent=Archivist,
        output_key='key_market_research'
    )
    
    # Business analysis tasks
    profile_competitor = Task(
        description="Based on the {key_market_research} and its analysis of relevant market segments, identify and create a detailed profile for the top 3-5 direct competitors to 'MostlyOpenAI' in the enterprise-grade LLM space (e.g., OpenAI's enterprise offerings, Google Cloud AI, Anthropic). For each competitor, focus on their key enterprise LLM products, reported pricing models (if public), target industries, strategic partnerships and actions, and recent significant announcements.",
        expected_output="""A JSON object with the following structure:
        {
          "competitors": [
            {
              "name": "string - competitor name",
              "company_overview": {
                "founded": "string - year founded",
                "headquarters": "string - location",
                "funding": "string - latest funding round",
                "valuation": "string - estimated valuation"
              },
              "enterprise_products": [
                {
                  "name": "string - product name",
                  "description": "string - product description",
                  "target_industries": ["string - target sectors"],
                  "key_features": ["string - main features"],
                  "pricing_model": "string - pricing structure",
                  "deployment_options": ["string - cloud|on_premise|hybrid"]
                }
              ],
              "pricing_analysis": {
                "base_pricing": "string - starting price",
                "enterprise_pricing": "string - enterprise tier pricing",
                "pricing_factors": ["string - factors affecting price"],
                "cost_comparison": "float - relative cost score (1-10)"
              },
              "market_position": {
                "target_segments": ["string - primary market segments"],
                "geographic_focus": ["string - target regions"],
                "competitive_advantages": ["string - key advantages"],
                "market_share_estimate": "string - estimated market share"
              },
              "strategic_partnerships": [
                {
                  "partner": "string - partner name",
                  "type": "string - partnership type",
                  "announcement_date": "string - YYYY-MM-DD",
                  "description": "string - partnership details"
                }
              ],
              "recent_announcements": [
                {
                  "date": "string - YYYY-MM-DD",
                  "title": "string - announcement title",
                  "summary": "string - brief summary",
                  "impact": "string - potential market impact"
                }
              ]
            }
          ],
          "comparative_analysis": {
            "pricing_comparison": {
              "labels": ["string - competitor names"],
              "values": ["float - relative pricing scores"]
            },
            "feature_comparison": {
              "labels": ["string - feature categories"],
              "competitors": {
                "competitor1": ["float - feature scores"],
                "competitor2": ["float - feature scores"]
              }
            },
            "market_focus": {
              "labels": ["string - market segments"],
              "competitors": {
                "competitor1": ["float - focus scores"],
                "competitor2": ["float - focus scores"]
              }
            }
          },
          "insights": {
            "key_differentiators": ["string - main differentiators"],
            "pricing_trends": "string - observed pricing patterns",
            "partnership_strategies": "string - partnership approach analysis",
            "recommendations": ["string - strategic recommendations for MostlyOpenAI"]
          }
        }""",
        context=[collect_reports_news],
        agent=Shadow,
        parallel=True,
        output_key='competitor_profiles'
    )
    
    analyze_comp_markt_position = Task(
        description="Examine the marketing messaging, public statements, and positioning strategies of the {competitor_profiles} you've identified. Identify their unique selling propositions (USPs) for enterprise clients, their ethical AI stances, and how they address concerns like data privacy, model explainability, and compliance in their public communications and product documentation.",
        expected_output="""A JSON object with the following structure:
        {
          "marketing_analysis": [
            {
              "competitor_name": "string - competitor name",
              "brand_positioning": {
                "primary_message": "string - main brand message",
                "target_audience": "string - primary target audience",
                "value_proposition": "string - core value proposition",
                "brand_personality": "string - brand characteristics"
              },
              "unique_selling_propositions": [
                {
                  "usp": "string - unique selling proposition",
                  "target_benefit": "string - benefit to enterprise clients",
                  "evidence": "string - supporting evidence or claims",
                  "differentiation": "string - how it differs from competitors"
                }
              ],
              "ethical_ai_stance": {
                "principles": ["string - ethical principles"],
                "transparency_approach": "string - transparency strategy",
                "bias_mitigation": "string - bias handling approach",
                "safety_measures": ["string - safety protocols"],
                "governance": "string - AI governance approach"
              },
              "data_privacy_approach": {
                "privacy_commitments": ["string - privacy promises"],
                "data_handling": "string - data processing approach",
                "compliance_frameworks": ["string - compliance standards"],
                "security_measures": ["string - security protocols"],
                "data_sovereignty": "string - data location policies"
              },
              "explainability_strategy": {
                "model_interpretability": "string - explainability approach",
                "audit_capabilities": "string - audit features",
                "documentation_quality": "string - documentation approach",
                "user_control": "string - user control features"
              },
              "compliance_focus": {
                "regulatory_compliance": ["string - compliance standards"],
                "industry_specific": ["string - industry compliance"],
                "certifications": ["string - relevant certifications"],
                "audit_readiness": "string - audit preparation approach"
              }
            }
          ],
          "comparative_metrics": {
            "ethical_focus_score": {
              "labels": ["string - competitor names"],
              "values": ["float - ethical focus scores (1-10)"]
            },
            "privacy_focus_score": {
              "labels": ["string - competitor names"], 
              "values": ["float - privacy focus scores (1-10)"]
            },
            "compliance_breadth": {
              "labels": ["string - competitor names"],
              "values": ["float - compliance breadth scores (1-10)"]
            },
            "transparency_score": {
              "labels": ["string - competitor names"],
              "values": ["float - transparency scores (1-10)"]
            }
          },
          "strategic_insights": {
            "positioning_gaps": ["string - market positioning opportunities"],
            "ethical_differentiation": "string - ethical positioning analysis",
            "privacy_advantages": ["string - privacy-related opportunities"],
            "compliance_opportunities": ["string - compliance advantages"],
            "messaging_recommendations": ["string - messaging strategy suggestions"]
          }
        }""",
        context=[profile_competitor],
        agent=Shadow,
        output_key='competitor_marketing_analysis'
    )
    
    # Trends and shifts analysis tasks
    identify_trends = Task(
        description="Analyze the {key_market_research} to pinpoint 3-5 cutting-edge technological advancements, new research paradigms (e.g., novel architectures, multimodal LLMs, efficient training methods), or significant shifts in LLM development that hold the highest potential to disrupt or redefine the enterprise LLM market in the next 1-3 years. Focus on trends with clear implications for 'MostlyOpenAI's' product roadmap or strategic direction.",
        expected_output="""A JSON object with the following structure:
        {
          "emerging_technologies": [
            {
              "name": "string - technology/trend name",
              "category": "string - architecture|training|deployment|application",
              "description": "string - detailed explanation",
              "current_state": {
                "development_stage": "string - research|prototype|early_adoption|mainstream",
                "key_players": ["string - leading companies/researchers"],
                "adoption_rate": "string - current adoption level"
              },
              "enterprise_impact": {
                "potential_benefits": ["string - benefits for enterprises"],
                "implementation_challenges": ["string - adoption challenges"],
                "cost_implications": "string - cost impact analysis",
                "timeline": "string - expected mainstream adoption timeline"
              },
              "disruption_potential": {
                "market_disruption_score": "float - 1-10 score",
                "competitive_advantage": "string - competitive implications",
                "risk_factors": ["string - potential risks"],
                "opportunity_areas": ["string - opportunity identification"]
              },
              "source_evidence": [
                {
                  "source": "string - source name",
                  "url": "string - source URL",
                  "key_finding": "string - relevant finding",
                  "credibility": "string - source credibility level"
                }
              ],
              "strategic_recommendations": {
                "immediate_actions": ["string - immediate strategic actions"],
                "research_priorities": ["string - research focus areas"],
                "partnership_opportunities": ["string - partnership suggestions"],
                "investment_considerations": "string - investment recommendations"
              }
            }
          ],
          "trend_analysis": {
            "adoption_timeline": {
              "labels": ["string - technology names"],
              "values": ["float - months to mainstream adoption"]
            },
            "impact_scores": {
              "labels": ["string - technology names"],
              "values": ["float - impact scores (1-10)"]
            },
            "investment_priority": {
              "labels": ["string - technology names"],
              "values": ["float - priority scores (1-10)"]
            }
          },
          "market_implications": {
            "short_term_impacts": ["string - 6-12 month impacts"],
            "medium_term_impacts": ["string - 1-2 year impacts"],
            "long_term_impacts": ["string - 3+ year impacts"],
            "competitive_landscape_changes": ["string - competitive implications"],
            "regulatory_considerations": ["string - regulatory impacts"]
          },
          "strategic_insights": {
            "technology_roadmap_suggestions": ["string - roadmap recommendations"],
            "resource_allocation": ["string - resource allocation advice"],
            "risk_mitigation": ["string - risk mitigation strategies"],
            "opportunity_maximization": ["string - opportunity strategies"]
          }
        }""",
        context=[collect_reports_news],
        agent=Seer,
        parallel=True,
        output_key='emerging_tech_trends'
    )
    
    identify_reg_ethic_shift = Task(
        description="Research and identify 2-3 significant emerging regulatory frameworks (e.g., AI Acts, data governance laws, industry-specific compliance standards) or evolving ethical considerations specifically impacting enterprise LLM deployment. Analyze their potential implications for 'MostlyOpenAI' and its clients, considering both challenges and opportunities.",
        expected_output="""A JSON object with the following structure:
        {
          "regulatory_frameworks": [
            {
              "name": "string - regulation name",
              "jurisdiction": "string - geographic scope",
              "status": "string - proposed|draft|enacted|enforced",
              "effective_date": "string - YYYY-MM-DD or timeline",
              "scope": {
                "applies_to": ["string - covered AI systems"],
                "exemptions": ["string - exempted systems"],
                "thresholds": "string - applicability thresholds"
              },
              "key_requirements": [
                {
                  "requirement": "string - specific requirement",
                  "description": "string - detailed explanation",
                  "compliance_complexity": "string - low|medium|high",
                  "implementation_cost": "string - estimated cost impact"
                }
              ],
              "enforcement_mechanisms": {
                "penalties": ["string - potential penalties"],
                "audit_requirements": "string - audit obligations",
                "reporting_obligations": ["string - reporting requirements"],
                "certification_needs": ["string - certification requirements"]
              },
              "impact_analysis": {
                "direct_impacts": ["string - direct effects on LLM providers"],
                "indirect_impacts": ["string - indirect effects"],
                "client_implications": ["string - effects on enterprise clients"],
                "competitive_implications": "string - competitive effects"
              }
            }
          ],
          "ethical_considerations": [
            {
              "ethical_principle": "string - ethical consideration name",
              "description": "string - detailed explanation",
              "current_standards": "string - existing ethical standards",
              "emerging_expectations": "string - evolving expectations",
              "implementation_challenges": ["string - implementation difficulties"],
              "best_practices": ["string - recommended practices"],
              "stakeholder_expectations": {
                "customers": "string - customer expectations",
                "employees": "string - employee expectations", 
                "investors": "string - investor expectations",
                "regulators": "string - regulatory expectations"
              }
            }
          ],
          "compliance_landscape": {
            "current_compliance": {
              "labels": ["string - compliance areas"],
              "values": ["float - current compliance scores (1-10)"]
            },
            "future_requirements": {
              "labels": ["string - future compliance areas"],
              "values": ["float - future requirement scores (1-10)"]
            },
            "compliance_gaps": {
              "labels": ["string - gap areas"],
              "values": ["float - gap severity scores (1-10)"]
            }
          },
          "strategic_implications": {
            "compliance_priorities": ["string - priority compliance areas"],
            "resource_requirements": {
              "legal_resources": "string - legal resource needs",
              "technical_resources": "string - technical resource needs",
              "operational_resources": "string - operational resource needs"
            },
            "timeline_considerations": {
              "immediate_actions": ["string - immediate compliance actions"],
              "short_term_goals": ["string - 6-12 month goals"],
              "long_term_strategy": ["string - long-term compliance strategy"]
            },
            "risk_assessment": {
              "high_risk_areas": ["string - high-risk compliance areas"],
              "medium_risk_areas": ["string - medium-risk areas"],
              "low_risk_areas": ["string - low-risk areas"],
              "mitigation_strategies": ["string - risk mitigation approaches"]
            }
          },
          "opportunity_analysis": {
            "competitive_advantages": ["string - compliance-based advantages"],
            "market_opportunities": ["string - new market opportunities"],
            "partnership_potential": ["string - partnership opportunities"],
            "innovation_areas": ["string - innovation opportunities"]
          }
        }""",
        context=[collect_reports_news],
        agent=Seer,
        parallel=True,
        output_key='regulatory_ethical_shifts'
    )
    
    # Summary tasks
    compile_all = Task(
        description="""Compile all insights and findings from the provided JSON contexts (competitor profiles, marketing analysis, 
        emerging trends, and regulatory shifts) into a single, comprehensive C-level executive report.
        Each JSON contains both 'plot_data' for charts and 'summary_text' for content.
        
        **Report Generation Process:**
        1. **Data Extraction & Chart Planning:** Iterate through each provided JSON context. Extract all 'plot_data' and 'summary_text' components. Identify key data points and suitable chart types (bar or line) for visualization based on the analysis.
        2. **Chart Creation:** For each identified 'plot_data', use the **'Generate Plot Image' tool** to create high-quality, relevant charts. Ensure each chart has a clear, descriptive title and appropriate axis labels. Save each chart image, making sure to track and remember all generated image file paths for later use.
        3. **Comprehensive Report Text Synthesis:** Consolidate ALL the extracted 'summary_text' components into one cohesive, professional, and concise markdown report. Structure the report to include:
           - An Executive Summary (1-2 paragraphs).
           - Dedicated sections for: 
             a. Competitor Landscape Analysis (integrating competitor profiles and marketing analysis, including strategic takeaways for 'MostlyOpenAI').
             b. Emerging Technologies & Trends (highlighting opportunities and potential disruptions from the emerging tech trends analysis).
             c. Regulatory & Ethical Implications (outlining compliance needs and ethical positioning from the regulatory/ethical shifts analysis).
           Explicitly reference each generated chart within the relevant sections (e.g., 'As shown in Figure 1, the Q3 growth trend...'). Ensure all relevant sources are clearly mentioned.
        4. **Intermediate Text Output:** Save this complete, synthesized markdown report text to a file using the **'File Write Tool'**. Name it 'executive_report_content.md' in the 'output/' directory.
        5. **Final PDF Assembly:** Utilize the **'Create PDF Report' tool**. Provide it with the path to the 'executive_report_content.md' file and the complete list of all chart image file paths generated. Title the final PDF 'Enterprise LLM Landscape: Executive Summary'. Save the final PDF as 'Enterprise_LLM_Report.pdf' in the 'output/reports/' directory.
        
        **The final output of this task MUST be the absolute file path to the completed PDF report.**""",
        expected_output="A string representing the absolute file path to the completed, visually rich PDF executive report, which includes all synthesized analysis, trends, shifts, and embedded charts. Example: 'output/reports/Enterprise_LLM_Report.pdf'",
        context=[identify_key_market_segments, collect_reports_news, profile_competitor, analyze_comp_markt_position, identify_trends, identify_reg_ethic_shift],
        agent=Nexus,
        output_file='output/reports/MostlyOpenAI_Market_Report.pdf',
        output_key='final_strategic_report'
    )
    
    return [
        identify_key_market_segments,
        collect_reports_news,
        profile_competitor,
        analyze_comp_markt_position,
        identify_trends,
        identify_reg_ethic_shift,
        compile_all
    ]


# Create default task instances
tasks = create_market_analysis_tasks()
identify_key_market_segments = tasks[0]
collect_reports_news = tasks[1]
profile_competitor = tasks[2]
analyze_comp_markt_position = tasks[3]
identify_trends = tasks[4]
identify_reg_ethic_shift = tasks[5]
compile_all = tasks[6] 