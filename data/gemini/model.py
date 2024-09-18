import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from apikey import API_KEY

genai.configure(api_key=API_KEY)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def list_all_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

def model(prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    val = to_markdown(response.text)
    print(response.prompt_feedback)
    return response.text






