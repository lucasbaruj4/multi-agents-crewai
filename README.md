# Multi-Agent Market Research System

A sophisticated multi-agent research system for enterprise LLM market analysis using CrewAI and optimized Gemini models.

## 🎯 **NEW: COMPANY PERSONALIZATION + OPTIMIZED API USAGE**

This system now features **company-specific personalization** with **executive-friendly questionnaire** and **optimized Gemini API usage** with **75-80% reduction** in token consumption while maintaining high-quality market analysis capabilities.

### **Key Features:**
- **Company Personalization**: Executive-friendly questionnaire for targeted research
- **Smart Context Injection**: Company-specific insights within token budget
- **7 tasks → 4 tasks** (43% reduction)
- **4 agents → 3 agents** (25% reduction)
- **Ultra-minimal token limits**: 150-300 tokens per task
- **Simplified JSON outputs** with focused structure
- **Expected usage**: 500-700 tokens per run (personalized insights)

## 🚀 Features

### **Company Personalization System**
- **Executive Questionnaire**: 5-section interactive CLI for company information
- **Smart Context Injection**: Company-specific insights in all agents and tasks
- **Profile Management**: Automatic persistence and loading of company profiles
- **Hybrid Integration**: Seamless experience with optional power commands

### **Multi-Agent Architecture**
- **Archivist**: Expert in finding relevant market data for your company
- **Shadow**: Expert in dissecting competitor strategies for your industry
- **Nexus**: Expert in concise and actionable reporting for your goals

### **Personalized Workflow**
1. **Company Profile Setup** (5-10 minutes, one-time)
2. **Market Segment Identification** (company-focused)
3. **Research Collection** (industry-specific)
4. **Competitor Analysis** (targeted to your competitors)
5. **Executive Summary** (strategic insights for your company)

### **Structured Outputs**
All tasks produce structured JSON outputs with specific schemas for efficient multi-agent workflows:
- Market segments with descriptions and sizes (relevant to your industry)
- Research sources with key findings (focused on your research areas)
- Competitor profiles with strengths and positions (targeting your competitors)
- Executive summaries with insights and recommendations (aligned with your strategic goals)

## 🛠️ Installation

### **Prerequisites**
- Python 3.8+
- Google API key (for Gemini model)
- SerperDev API key (for web search)
- Firecrawl API key (for web scraping)

### **Setup**
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Multi-AI-Agent-Systems-with-CrewAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env.local` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   ```

## 🎯 Usage

### **Quick Start (Executive Experience)**
```bash
python main.py
```

The system will:
1. **First Time**: Guide you through a 5-10 minute company profile questionnaire
2. **Returning**: Load your existing company profile (or offer to update it)
3. Load environment variables from `.env.local`
4. Test Gemini integration
5. Create personalized agents and tasks for your company
6. Execute targeted market analysis workflow
7. Generate company-specific structured results

### **Power User Commands**
```bash
# Run questionnaire only
python main.py --questionnaire-only

# Skip questionnaire, use existing profile
python main.py --skip-questionnaire

# Force creation of new company profile
python main.py --new-profile
```

### **Expected Output (Personalized)**
```json
{
  "summary": {
    "key_insights": [
      "For [Your Company] in [Your Industry], the LLM market shows...",
      "Your target customers are increasingly adopting AI solutions...",
      "Your competitors [Competitor Names] are focusing on..."
    ],
    "competitive_landscape": "In your market position as [Position], you face competition from...",
    "recommendations": [
      "Given your strategic goals of [Goals], prioritize...",
      "To address your challenges of [Challenges], consider...",
      "For your research focus areas of [Focus Areas], explore..."
    ]
  }
}
```

## 📁 Project Structure

```
Multi AI-Agent Systems with CrewAI/
├── src/
│   ├── agents/           # Agent definitions (Archivist, Shadow, Nexus)
│   ├── tasks/            # Market analysis tasks (4 optimized tasks)
│   ├── llm/              # LLM integration (Gemini optimized)
│   ├── tools/            # Utility tools (PDF, plotting)
│   ├── company_profile/  # Company profile management & questionnaire
│   └── templates/        # Context injection & template management
├── mistral_connection/   # Archived Mistral files for rollback
├── output/               # Generated reports and charts
├── config/               # Configuration files (including company_profile.json)
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── main.py               # Main execution script
├── requirements.txt      # Dependencies
└── .env.local           # Environment variables (not in git)
```

## 🔧 Configuration

### **API Keys Required**
- **GOOGLE_API_KEY**: For Gemini model access
- **SERPER_API_KEY**: For web search capabilities
- **FIRECRAWL_API_KEY**: For web scraping

### **Model Configuration**
The system uses `gemini/gemini-2.0-flash-lite` for optimal cost efficiency with:
- Temperature: 0.1-0.3 (focused responses)
- Max tokens: 150-300 (strict limits)
- Timeout: 60 seconds

## 📊 Performance

### **Personalization Results**
- **Company Context**: Smart injection within 100-150 token budget per task
- **Executive Experience**: 5-10 minute questionnaire for complete personalization
- **Profile Management**: Automatic persistence and seamless loading
- **Quality Improvement**: Highly targeted insights vs generic analysis

### **Optimization Results**
- **API Usage**: 75-80% reduction achieved (500-700 tokens vs 2000-3000)
- **Task Completion**: All 4 tasks complete successfully with personalization
- **Response Quality**: High-quality structured outputs with company context
- **Cost Efficiency**: Minimal token consumption with maximum personalization

### **System Capabilities**
- **Personalized Market Analysis**: Company-specific enterprise LLM market insights
- **Targeted Competitive Intelligence**: Analysis focused on your competitors
- **Strategic Recommendations**: Actionable insights aligned with your goals
- **Structured Outputs**: JSON-formatted results with company context

## 🔄 Rollback to Mistral

If you need to switch back to the Mistral setup:
1. All Mistral files are preserved in `mistral_connection/` folder
2. Update imports to use Mistral components
3. Configure Colab server connection
4. Update environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with minimal API usage
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation in `docs/`
2. Review the chat log in `.cursor/chatlog.md`
3. Check task status in `.cursor/tasks.md`
4. Open an issue on GitHub

---

**Status**: ✅ **PRODUCTION READY** - Company personalization + optimized API usage with high-quality targeted results 