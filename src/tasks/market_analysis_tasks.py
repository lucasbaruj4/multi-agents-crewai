"""
Market Analysis Tasks Module
===========================

Market analysis tasks and workflows for the multi-agent research system.
"""

from crewai import Task
from ..agents import Archivist, Shadow, Seer, Nexus


def create_market_analysis_tasks():
    """
    Create all market analysis tasks for the crew
    
    Returns:
        List of configured tasks
    """
    
    # Research tasks
    identify_key_market_segments = Task(
        description="Identify and list the primary market segments within the enterprise-grade LLM industry (e.g., finance, healthcare, legal, specialized customer service, R&D). For each segment, provide a brief overview of its specific LLM needs and growth potential.",
        expected_output="Format JSON, A structured list of 3-5 key enterprise LLM market segments, with a 1-2 paragraph summary for each, including estimated market size and growth rates if available. Name the output 'key_market_segments'",
        agent=Archivist,
        output_key='key_market_segments'
    )
    
    collect_reports_news = Task(
        description="""Conduct an exhaustive search for the most recent and highly relevant industry reports, whitepapers, research papers, academic studies, and significant news articles (published within the last 4 months) pertaining to the enterprise-grade LLM market. Focus specifically on: 1. Adoption rates and success stories within the previously identified market segments. 2. Technological advancements and new model architectures relevant to enterprise deployment (e.g., efficiency, fine-tuning, security). 3. Specific use cases and implementation challenges faced by businesses within these segments. 4. Market dynamics, investment trends, and significant partnerships within the LLM ecosystem. Prioritize information from top-tier technology research firms, leading academic institutions, and highly reputable industry news sources. The goal is to gather a diverse and comprehensive collection of foundational documents.""",
        expected_output="Format JSON, A curated, categorized list of high-quality external resources (links to PDFs or web articles). Each link must be accompanied by a concise summary highlighting its main findings or key contribution to understanding the enterprise LLM market within the specified segments. The collection should be sufficiently broad and deep to inform subsequent detailed analysis by other agents. Name the output: 'key_market_research'",
        context=[identify_key_market_segments],
        agent=Archivist,
        output_key='key_market_research'
    )
    
    # Business analysis tasks
    profile_competitor = Task(
        description="Based on the {key_market_research} and its analysis of relevant market segments, identify and create a detailed profile for the top 3-5 direct competitors to 'MostlyOpenAI' in the enterprise-grade LLM space (e.g., OpenAI's enterprise offerings, Google Cloud AI, Anthropic). For each competitor, focus on their key enterprise LLM products, reported pricing models (if public), target industries, strategic partnerships and actions, and recent significant announcements.",
        expected_output="""A JSON object structured with two main keys: 'plot_data' and 'summary_text'.
        The 'plot_data' key should contain a dictionary suitable for plotting, with 'labels' (List[str] of competitor names)
        and 'values' (List[float] of a key comparable metric like 'average reported pricing' or 'number of features', whichever is most appropriate for a single plot).
        The 'summary_text' key should contain a comprehensive markdown string detailing each competitor's profile, including
        product names, features, pricing, clients/industries, and collaborations.

        Example:
        {
          "plot_data": {
            "labels": ["CompA", "CompB", "CompC"],
            "values": [50000.0, 75000.0, 60000.0]
          },
          "summary_text": "## Competitor Profiles\\n\\n### CompA\\n- Product: AlphaLLM\\n- Features: Scalability, Customization, Fine-tuning\\n- Pricing: ~$50,000/year (reported)\\n- Clients: Finance, Healthcare\\n- Collaborations: CloudCorp\\n\\n### CompB\\n- Product: BetaAI\\n- Features: Multimodal, Real-time processing\\n- Pricing: ~$75,000/year (reported)\\n- Clients: Retail, Automotive\\n- Collaborations: DataSolutions\\n\\n### CompC\\n- Product: GammaGen\\n- Features: Security, On-premise deployment\\n- Pricing: ~$60,000/year (reported)\\n- Clients: Government, Defense\\n- Collaborations: CyberSec Inc."
        }
        """,
        context=[collect_reports_news],
        agent=Shadow,
        parallel=True,
        output_key='competitor_profiles'
    )
    
    analyze_comp_markt_position = Task(
        description="Examine the marketing messaging, public statements, and positioning strategies of the {competitor_profiles} you've identified. Identify their unique selling propositions (USPs) for enterprise clients, their ethical AI stances, and how they address concerns like data privacy, model explainability, and compliance in their public communications and product documentation.",
        expected_output="""A JSON object structured with two main keys: 'plot_data' and 'summary_text'.
        The 'plot_data' key should contain a dictionary suitable for plotting, with 'labels' (List[str] of competitor names)
        and 'values' (List[float] representing a quantifiable comparative metric like 'score for data privacy focus',
        'number of stated USPs', or 'overall ethical emphasis score').
        The 'summary_text' key should contain a comprehensive markdown string detailing the comparative marketing analysis,
        including specific examples of USPs, ethical principles, and data privacy/explainability approaches for each competitor.

        Example:
        {
          "plot_data": {
            "labels": ["CompA", "CompB", "CompC"],
            "values": [8.5, 7.0, 9.2]
          },
          "summary_text": "## Competitor Marketing & Positioning Analysis\\n\\n### CompA\\n- **USP:** 'Hyper-Scalable AI for Enterprise Growth'\\n- **Ethical Stance:** Emphasizes 'Responsible AI deployment with human oversight'.\\n- **Data Privacy:** Strong focus on 'on-premise deployment options and certified data isolation'.\\n\\n### CompB\\n- **USP:** 'AI for Seamless Multimodal Interaction'\\n- **Ethical Stance:** Highlights 'AI fairness and bias mitigation through audited datasets'.\\n- **Data Privacy:** Advocates for 'federated learning to protect sensitive client data'."
        }
        """,
        context=[profile_competitor],
        agent=Shadow,
        output_key='competitor_marketing_analysis'
    )
    
    # Trends and shifts analysis tasks
    identify_trends = Task(
        description="Analyze the {key_market_research} to pinpoint 3-5 cutting-edge technological advancements, new research paradigms (e.g., novel architectures, multimodal LLMs, efficient training methods), or significant shifts in LLM development that hold the highest potential to disrupt or redefine the enterprise LLM market in the next 1-3 years. Focus on trends with clear implications for 'MostlyOpenAI's' product roadmap or strategic direction.",
        expected_output="""A JSON object structured with two main keys: 'plot_data' and 'summary_text'.
        The 'plot_data' key should contain a dictionary suitable for plotting, with 'labels' (List[str] of trend names)
        and 'values' (List[float] representing a quantifiable priority score, impact score, or adoption rate potential).
        The 'summary_text' key should contain a comprehensive markdown string detailing each emerging technology/research trend,
        including its explanation, potential enterprise impact, and specific source citations.

        Example:
        {
          "plot_data": {
            "labels": ["RAG", "MoE", "Small LLMs"],
            "values": [9.0, 8.5, 7.5]
          },
          "summary_text": "## Emerging LLM Technologies & Trends\\n\\n### 1. Retrieval-Augmented Generation (RAG)\\n- **Explanation:** Combines LLMs with external knowledge bases to provide up-to-date and factual responses.\\n- **Impact:** Reduces hallucinations, provides citations, ideal for enterprise knowledge management.\\n- **Sources:** Smith et al. (2023) 'RAG in Practice'.\\n\\n### 2. Mixture-of-Experts (MoE) Architectures\\n- **Explanation:** LLMs with specialized 'expert' subnetworks activated selectively per query, improving efficiency and scalability.\\n- **Impact:** More cost-effective, faster inference for large models, enabling larger scale enterprise deployments.\\n- **Sources:** Google DeepMind (2024) 'Scaling MoE Models'."
        }
        """,
        context=[collect_reports_news],
        agent=Seer,
        parallel=True,
        output_key='emerging_tech_trends'
    )
    
    identify_reg_ethic_shift = Task(
        description="Research and identify 2-3 significant emerging regulatory frameworks (e.g., AI Acts, data governance laws, industry-specific compliance standards) or evolving ethical considerations specifically impacting enterprise LLM deployment. Analyze their potential implications for 'MostlyOpenAI' and its clients, considering both challenges and opportunities.",
        expected_output="""A JSON object structured with two main keys: 'plot_data' and 'summary_text'.
        The 'plot_data' key should contain a dictionary suitable for plotting, with 'labels' (List[str] of regulatory/ethical trend names)
        and 'values' (List[float] representing a quantifiable impact score, urgency level, or perceived risk).
        The 'summary_text' key should contain a comprehensive markdown string detailing each regulatory or ethical trend,
        including its nature, potential impact on LLM development/deployment, and direct implications for enterprise LLM providers.

        Example:
        {
          "plot_data": {
            "labels": ["AI Act (EU)", "Data Sovereignty", "Bias Audits"],
            "values": [9.5, 8.0, 7.0]
          },
          "summary_text": "## Regulatory & Ethical Shifts in LLMs\\n\\n### 1. EU AI Act\\n- **Nature:** Comprehensive regulation classifying AI systems by risk level.\\n- **Impact:** Stricter compliance, increased development costs, potential market fragmentation.\\n- **Implications for MostlyOpenAI:** Requires extensive legal review, robust risk assessment frameworks, and potential re-design of high-risk components.\\n\\n### 2. Data Sovereignty Movement\\n- **Nature:** Demand for data to be processed and stored within national borders.\\n- **Impact:** Challenges global cloud LLM deployments, necessitates regional data centers.\\n- **Implications for MostlyOpenAI:** Need for localized infrastructure, data governance compliance for specific regions."
        }
        """,
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