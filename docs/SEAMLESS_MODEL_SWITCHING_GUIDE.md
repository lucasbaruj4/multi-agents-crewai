# Seamless Model Switching Guide

## 🎯 **Overview**

The Multi-Agent Research System now supports **seamless model switching** between 4 major LLM providers. Simply change your API key in `.env.local` and the system automatically detects and uses the new provider - **no code changes needed!**

## 🚀 **Supported Providers**

| Provider | API Key Variable | Default Model | Cost Efficiency |
|----------|------------------|---------------|-----------------|
| **Google Gemini** | `GEN_MODEL_API` | `gemini-2.0-flash-lite` | High |
| **OpenAI** | `OPENAI_API_KEY` | `gpt-3.5-turbo` | High |
| **Anthropic** | `ANTHROPIC_API_KEY` | `claude-3-haiku` | High |
| **Mistral** | `MISTRAL_API_KEY` | `mistral-medium` | High |

## 🔄 **How to Switch Models**

### **Step 1: Update your `.env.local` file**

**Switch to OpenAI:**
```env
# Comment out or remove other LLM keys
# GEN_MODEL_API=your_gemini_key
OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key
# MISTRAL_API_KEY=your_mistral_key

# Keep web search keys
SERPER_API_KEY=your_serper_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

**Switch to Anthropic:**
```env
# GEN_MODEL_API=your_gemini_key
# OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
# MISTRAL_API_KEY=your_mistral_key

SERPER_API_KEY=your_serper_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

**Switch to Mistral:**
```env
# GEN_MODEL_API=your_gemini_key
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key
MISTRAL_API_KEY=your_mistral_key

SERPER_API_KEY=your_serper_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

### **Step 2: Run the system**

```bash
python main.py
```

The system will automatically:
- ✅ Detect your new provider
- ✅ Show provider information
- ✅ Use the most cost-efficient model
- ✅ Maintain all optimizations

## 🧪 **Testing Model Switching**

Run the test script to verify your setup:

```bash
python test_model_switching.py
```

This will show:
- Available providers
- Current provider and model
- Cost efficiency rating
- LLM creation tests

## 💰 **Cost Optimization**

Each provider uses the most cost-efficient model by default:

- **Gemini**: `gemini-2.0-flash-lite` (high efficiency)
- **OpenAI**: `gpt-3.5-turbo` (high efficiency)
- **Anthropic**: `claude-3-haiku` (high efficiency)
- **Mistral**: `mistral-medium` (high efficiency)

## 🔧 **Technical Details**

### **Automatic Detection**
The system uses `ModelConfig.get_available_providers()` to detect which API keys are set and automatically selects the first available provider.

### **Unified Interface**
All agents use the same functions regardless of provider:
- `create_strict_llm()` - For minimal token usage
- `create_standard_llm()` - For balanced usage
- `create_llm()` - For custom settings

### **Backward Compatibility**
All existing code continues to work. The system maintains backward compatibility with the old Gemini-specific functions.

## 📊 **System Information**

When you run the system, it shows:
```
✅ LLM Provider: Google Gemini (gemini-2.0-flash-lite)
✅ Cost Efficiency: high
```

## 🎯 **Benefits**

- **Zero Code Changes**: Switch providers by changing API key only
- **Automatic Detection**: System finds and uses available providers
- **Cost Optimized**: Each provider uses most efficient model
- **Quality Preserved**: High-quality results across all providers
- **Backward Compatible**: Existing code continues to work

## 🚨 **Troubleshooting**

**No providers available:**
```
❌ No LLM providers available
Please set one of: GEN_MODEL_API, OPENAI_API_KEY, ANTHROPIC_API_KEY, MISTRAL_API_KEY
```

**Solution:** Set one of the supported API keys in your `.env.local` file.

**Provider not available:**
```
❌ Provider 'openai' not available. Missing API key: OPENAI_API_KEY
```

**Solution:** Check that your API key is correctly set in `.env.local`.

## 📈 **Performance**

The system maintains the same optimizations across all providers:
- **75-80% token reduction** preserved
- **500-700 tokens per run** (personalized insights)
- **Ultra-minimal token limits**: 150-300 tokens per task
- **Simplified JSON outputs** with focused structure

---

**🎉 You can now seamlessly switch between any of the 4 major LLM providers by simply changing your API key!** 