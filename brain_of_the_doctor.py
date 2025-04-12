from dotenv import load_dotenv
load_dotenv()

import os
import base64
from groq import Groq

# Step 1: Setup GROQ API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Step 2: Convert image to base64
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None

# Step 3: Setup Multimodal LLM
query = "Is there something wrong with my face?"
model = "llama-3.2-90b-vision-preview"

def analyze_image_with_query(query, model, encoded_image):
    if not encoded_image:
        return "Failed to encode image."
    
    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": query },
                {
                    "type": "image_url",
                    "image_url": { "url": f"data:image/jpeg;base64,{encoded_image}" },
                },
            ],
        }
    ]
    
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error during API request: {str(e)}"

# Step 4: Use image and function
image_path = "test_face.jpg"
encoded_image = encode_image(image_path)
print(analyze_image_with_query(query, model, encoded_image))