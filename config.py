OLLAMA_MODELS = {
    "Deepseek R1 (1.3B - 1.3GB)": {"llm_model": "deepseek-r1:latest"},
    "Llama 3.2 (3B - 2.0GB)": {"llm_model": "llama3.2"},
    "Llama 3.2 (1B - 1.3GB)": {"llm_model": "llama3.2:1b"},
    "Llama 3.1 (8B - 4.7GB)": {"llm_model": "llama3.1"},
    "Llama 3.1 (70B - 40GB)": {"llm_model": "llama3.1:70b"},
    "Llama 3.1 (405B - 231GB)": {"llm_model": "llama3.1:405b"},
    "Phi 3 Mini (3.8B - 2.3GB)": {"llm_model": "phi3"},
    "Phi 3 Medium (14B - 7.9GB)": {"llm_model": "phi3:medium"},
    "Gemma 2 (2B - 1.6GB)": {"llm_model": "gemma2:2b"},
    "Gemma 2 (9B - 5.5GB)": {"llm_model": "gemma2"},
    "Gemma 2 (27B - 16GB)": {"llm_model": "gemma2:27b"},
    "Mistral (7B - 4.1GB)": {"llm_model": "mistral"},
    "Moondream 2 (1.4B - 829MB)": {"llm_model": "moondream"},
    "Neural Chat (7B - 4.1GB)": {"llm_model": "neural-chat"},
    "Starling (7B - 4.1GB)": {"llm_model": "starling-lm"},
    "Code Llama (7B - 3.8GB)": {"llm_model": "codellama"},
    "Llama 2 Uncensored (7B - 3.8GB)": {"llm_model": "llama2-uncensored"},
    "LLaVA (7B - 4.5GB)": {"llm_model": "llava"},
    "Solar (10.7B - 6.1GB)": {"llm_model": "solar"}
}

ONLINE_MODELS = {
    "GPT-4o": {
        "llm_model": "chatgpt-4o-latest",
        "embedding_model": "text-embedding-3-large",
        "dimensions": 3072
    },
    "GPT-4o Mini": {
        "llm_model": "gpt-4o-mini",
        "embedding_model": "text-embedding-3-large",
        "dimensions": 3072
    },
    "Gemini 2.0 Flash": {
        "llm_model": "gemini-2.0-flash-exp",
        "embedding_model": "text-embedding-004",
        "dimensions": 768
    },
    "Gemini 1.5 Pro": {
        "llm_model": "gemini-1.5-pro",
        "embedding_model": "text-embedding-004",
        "dimensions": 768
    },
    "Gemini 1.5 Flash": {
        "llm_model": "gemini-1.5-flash",
        "embedding_model": "text-embedding-004",
        "dimensions": 768
    },
}