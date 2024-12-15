
from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import requests
from dataclasses import dataclass

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

@dataclass
class LLMConfig:
    base_url: str
    model: str

def get_llm_response(prompt: str, config: LLMConfig) -> str:
    api_key = os.getenv('LLM_API_KEY')
    if not api_key:
        return "Error: API key not found in .env file. Please add LLM_API_KEY="
    
    # Clean up base URL
    base_url = config.base_url.rstrip('/')
    if not ('/completions' in base_url or '/chat/completions' in base_url):
        base_url += '/chat/completions'
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key.strip()}"
    }
    
    try:
        # Try chat endpoint first
        payload = {
            "model": config.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        
        response = requests.post(
            base_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # If chat endpoint fails, try completions
        if response.status_code in [404, 400, 401]:
            if '/chat/completions' in base_url:
                base_url = base_url.replace('/chat/completions', '/completions')
                payload = {
                    "model": config.model,
                    "prompt": prompt,
                    "max_tokens": 1000
                }
                response = requests.post(
                    base_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
        
        response.raise_for_status()
        data = response.json()
        
        # Handle response formats
        if "choices" in data:
            choice = data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"]
            if "text" in choice:
                return choice["text"]
        
        return f"Unexpected API response format: {str(data)}"
        
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if "401" in error_msg:
            return "Error: Invalid API key or unauthorized access"
        if "404" in error_msg:
            return "Error: Invalid API endpoint URL"
        return f"API Request Error: {error_msg}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        config = LLMConfig(
            base_url=request.form.get('base_url', '').strip(),
            model=request.form.get('model', '').strip()
        )
        session['llm_config'] = {
            'base_url': config.base_url,
            'model': config.model
        }
    config = session.get('llm_config')
    return render_template('index.html', config=config)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    config_dict = session.get('llm_config')
    if not config_dict:
        return render_template('index.html', 
                             result="Please configure LLM provider first")
    
    config = LLMConfig(**config_dict)
    item1 = request.form.get('item1', '').strip()
    item2 = request.form.get('item2', '').strip()
    
    if not item1 or not item2:
        return render_template('index.html', 
                             result="Please provide both items",
                             config=config)
    
    prompt = f"""Analyze the potential connections between '{item1}' and '{item2}'. 
Consider:
1. Direct relationships
2. Historical connections
3. Conceptual similarities
4. Shared characteristics

Format the response in a clear, structured way."""
    
    analysis = get_llm_response(prompt, config)
    return render_template('index.html', 
                         result=analysis,
                         item1=item1,
                         item2=item2,
                         config=config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
