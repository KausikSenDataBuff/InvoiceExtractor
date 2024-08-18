import google.generativeai as genai
gemini_multi_modal = 'gemini-1.5-flash-latest'
def gemini_config(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(gemini_multi_modal)
    return model

## Function to load OpenAI model and get respones

def get_genai_response(model,input,image,prompt):    
    response = model.generate_content([input,image,prompt])
    return response.text

### Function to read prompt
def get_prompt(file_path):
    with open(file_path, 'r') as f:
        prompt = f.read()
    return prompt