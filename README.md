# Multi-Agent Research System with CrewAI

A sophisticated multi-agent system for enterprise LLM market analysis, powered by CrewAI and a Colab-hosted Mistral model.

## 🚀 Features

- **Multi-Agent Architecture**: 4 specialized agents working together
- **Colab Integration**: Run powerful LLMs on Google Colab GPU without local resources
- **Market Analysis**: Comprehensive competitor and trend analysis
- **Report Generation**: Automated PDF reports with charts and visualizations
- **Modular Design**: Clean, maintainable codebase following software engineering best practices

## 🤖 Agents

1. **Archivist**: Expert in finding relevant market data and industry reports
2. **Shadow**: Specialist in dissecting competitor strategies and positioning
3. **Seer**: Analyst identifying emerging trends and technological shifts
4. **Nexus**: Chief insights architect creating executive reports

## 📋 Tasks

The system performs 7 sequential tasks:
1. Market segment identification
2. Industry research and news collection
3. Competitor profiling
4. Marketing position analysis
5. Emerging technology trends
6. Regulatory and ethical shifts
7. Executive report compilation

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Google Colab Pro (recommended) or free tier
- API keys for:
  - SerperDev (web search)
  - Google API (optional backup)
  - Firecrawl (web scraping)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd multi-agent-research-system
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:
   
   **Option A: Environment Variables (Local)**
   ```bash
   export SERPER_API_KEY="your_serper_api_key"
   export GOOGLE_API_KEY="your_google_api_key"
   export FIRECRAWL_API_KEY="your_firecrawl_api_key"
   ```
   
   **Option B: Colab Secrets (Recommended)**
   - In your Colab notebook, go to Settings → Secrets
   - Add your API keys with the same names

## 🚀 Quick Start

### 1. Start the Colab Server

Create a new Colab notebook and run the setup cells:

```python
# Cell 1: Install dependencies
!pip install transformers torch accelerate flask flask-cors

# Cell 2: Load Mistral model
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Cell 3: Create Flask API server
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model": model_name})

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 512)
    temperature = data.get('temperature', 0.5)
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# Cell 4: Install and start localtunnel
!npm install -g localtunnel
!lt --port 8081 --subdomain mistral-server &
```

### 2. Update Connection URL

Update `config/connection_credentials.py` with your localtunnel URL:

```python
COLAB_MISTRAL_URL = "https://your-subdomain.loca.lt"
```

### 3. Run the Analysis

```bash
python main.py
```

## 📁 Project Structure

```
multi-agent-research-system/
├── src/                          # Modular source code
│   ├── agents/                   # CrewAI agents
│   │   ├── archivist.py         # Market data expert
│   │   ├── shadow.py            # Competitor analyst
│   │   ├── seer.py              # Trend forecaster
│   │   └── nexus.py             # Report architect
│   ├── tasks/                   # Analysis tasks
│   │   └── market_analysis_tasks.py
│   ├── tools/                   # Custom tools
│   │   ├── plot_tools.py        # Chart generation
│   │   └── pdf_tools.py         # PDF creation
│   └── llm/                     # LLM integration
│       └── colab_mistral_llm.py
├── config/                       # Configuration files
│   ├── connection_credentials.py # Centralized connection settings
│   └── __init__.py
├── scripts/                      # Utility scripts
│   ├── local_mistral_client.py  # Colab connection client
│   └── __init__.py
├── docs/                         # Documentation
│   └── README_COLAB_CONNECTION.md
├── output/                       # Generated outputs
│   ├── charts/                  # Generated charts
│   ├── reports/                 # PDF reports
│   └── logs/                    # Execution logs
├── legacy_notebook/             # Original Jupyter notebook
├── .cursor/                     # Cursor IDE context (gitignored)
├── main.py                      # Main execution script
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔧 Configuration

### Connection Settings

All connection settings are centralized in `config/connection_credentials.py`:

```python
# Colab server URL
COLAB_MISTRAL_URL = "https://your-subdomain.loca.lt"

# API endpoints
HEALTH_ENDPOINT = f"{COLAB_MISTRAL_URL}/health"
GENERATE_ENDPOINT = f"{COLAB_MISTRAL_URL}/generate"

# Connection headers and timeouts
LOCALTUNNEL_HEADERS = {...}
DEFAULT_TIMEOUT = 60
```

### Customization

- **Agents**: Modify agent roles, goals, and backstories in `src/agents/`
- **Tasks**: Adjust task descriptions and expected outputs in `src/tasks/`
- **Tools**: Add new tools in `src/tools/`
- **LLM**: Switch models by updating `src/llm/colab_mistral_llm.py`

## 📊 Output

The system generates:

1. **Charts**: PNG files in `output/charts/`
2. **Reports**: PDF files in `output/reports/`
3. **Logs**: Detailed execution logs in `output/logs/`

## 🐛 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Ensure Colab server is running
   - Check localtunnel URL in `config/connection_credentials.py`
   - Verify firewall settings

2. **API Key Errors**
   - Set environment variables or Colab secrets
   - Check API key validity

3. **Memory Issues**
   - Use Colab Pro for better resources
   - Reduce model size or batch size

### Debug Mode

Enable verbose logging:

```python
# In main.py
crew = Crew(
    agents=[archivist, shadow, seer, nexus],
    tasks=tasks,
    process=Process.sequential,
    verbose=True  # Enable detailed logging
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [Mistral AI](https://mistral.ai/) for the language model
- [Google Colab](https://colab.research.google.com/) for GPU resources
- [Localtunnel](https://github.com/localtunnel/localtunnel) for secure tunneling

## 📞 Support

For questions and support:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the documentation in `docs/` 