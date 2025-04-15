import requests
import os
from dotenv import load_dotenv
import json
import sys
from time import sleep
import re

load_dotenv()

# Retrieve your Groq API key from an environment variable
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Please set the GROQ_API_KEY environment variable")

url = "https://api.groq.com/openai/v1/chat/completions"

# Define the models to use for the API
ai_models = {
    "thinking": "deepseek-r1-distill-llama-70b",
    "normal": "llama-3.3-70b-specdec"
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def groq_title_divider(prompt: str, thinking_model: bool = False, retry:int=0) -> list[str] | None:
    """
    This function divides the input text into two meaningful parts using the Groq API.
    If the division fails, it retries with a different model.
    Args:
        prompt (str): The input text to be divided.
        thinking_model (bool): Whether to use the thinking model or not.
        retry (int): The number of retries attempted.
    Returns:
        list[str] | None: The divided titles or None if the division fails.
    """

    if retry > 5:
        print("\033[31mTitle division failed.\033[0m")
        return None

    print("\033[32mpreparing title...\033[0m")
    payload = {
        "model": ai_models["thinking"] if thinking_model else ai_models["normal"],
        "messages": [
            {
                "role": "user",
                "content": f'{PromptExtension["title_divider"]}\n\ntext: {prompt}'
            }
        ]
    }

    # Send the POST request to the API
    
    print("\033[32mgetting title divide response...\033[0m")
    response = requests.post(url, headers=headers, json=payload)


    if response.status_code == 200:
        content: str = response.json()["choices"][0]["message"]["content"]
        print("title_divide:", content)
        print("\033[32mprocessing titles...\033[0m")

        if thinking_model:
            titles = re.split(r"\n", content.split("</think>")[1].strip())
        else:
            titles = re.split(r"\n", content.strip())
        returnable_data = []
        for title in titles:
            title = title.strip()
            if title:
                returnable_data.append(title)

        if len(returnable_data) != 2:
            print(returnable_data)
            print("\033[31mTitle division failed.\033[0m")
            print("\033[32mchanging model...\033[0m")
            thinking_model = not thinking_model
            print("\033[32mtrying again...\033[0m")
            return groq_title_divider(prompt, thinking_model, retry+1)
        
        print("\033[32mdivided titles: \033[0m",returnable_data)
        return returnable_data
    else:
        print(response.text)
        return groq_title_divider(prompt, thinking_model, retry+1)

def groq_prompt_gen(prompt: list[str], thinking_model=False, retry:int=0) -> str | None:
    """
    This function generates an image prompt from the divided titles using the Groq API.
    If the generation fails, it retries with a different model.
    Args:
        prompt (list[str]): The divided titles to be used for prompt generation.
        thinking_model (bool): Whether to use the thinking model or not.
        retry (int): The number of retries attempted.
    Returns:
        str | None: The generated image prompt or None if the generation fails.
    """
    if retry > 5:
        print("\033[31mImage prompt generation failed.\033[0m")
        return None
    
    print("Title Prepared.")
    print("\033[32mGenerating prompt...\033[0m")
    payload = {
        "model": ai_models["thinking"] if thinking_model else ai_models["normal"],
        "messages": [
            {
                "role": "user",
                "content": f'{PromptExtension["prompt_creator"]}\n\n"{prompt[0]}" "{prompt[1]}"'
            }
        ]
    }

    # Send the POST request to the API
    print("\033[32mgetting image prompt response...\033[0m")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        content: str = response.json()["choices"][0]["message"]["content"]
        print("image_prompt_data:", content)
        
        if thinking_model:
            image_prompt: str = content.split("</think>")[1].replace("\n", "").strip()
        else:
            image_prompt: str = content.replace("\n", "").strip()
        print("image_prompt: \033[32m", image_prompt, "\033[0m")
        return image_prompt
    else:
        print(response.text)
        # sys.exit(f"Request failed with status code {response.status_code}")
        return groq_prompt_gen(prompt, thinking_model=not thinking_model, retry=retry+1)

PromptExtension = {
    "title_divider": """Split the input text into two appropriate or meaningful parts, only if no good spliting points found then split before a preposition. Don't alter words (e.g. preposition stays). Remove colons, periods, and emojis. Output the result in uppercase on two lines (separated by `\\n`), with no other text.""",
    "prompt_creator": """Generate a 3-line image prompt from two input texts:
1.  **Line 1:** Describe the first input text, including a style (font/color/design).
2.  **Line 2:** Describe the second input text, including a style (font/color/design).
3.  **Line 3:** Add a short, vague, related background description.

**Output *only* the 3-line prompt, without explanation.**

**(Example Input: 'GOODBYE FEBRUARY, HELLO MARCH!', 'EMBRACE NEW BEGINNINGS')**
**Example Output:**
a social media image with text overlay 'GOODBYE FEBRUARY, HELLO MARCH!' written in clear font in icy blue and warm orange. Elegant cursive smaller phrase 'EMBRACE NEW BEGINNINGS' in soft pastel tones with subtle sparkles. March and spring themed background."""
    }