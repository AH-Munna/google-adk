import os
from dotenv import load_dotenv

load_dotenv()

targon_api_key = os.getenv("targon")
chutes_api_key = os.getenv("chutes")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# from openai import OpenAI

# client = OpenAI(
#     api_key="",
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# response = client.chat.completions.create(
#     model="gemini-2.0-flash",
#     n=1,
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Explain to me how AI works"
#         }
#     ]
# )

# print(response.choices[0].message)

# # pdf maker
# from fpdf import FPDF

# # Define the summer bucket list items
# bucket_list_items = [
#     "Have a picnic in the park",
#     "Go on a nature hike",
#     "Visit a local farmers market",
#     "Watch the sunset with friends",
#     "Try a new ice cream flavor",
#     "Have a water balloon fight",
#     "Go camping (even in your backyard!)",
#     "Create a summer photo journal",
#     "Make homemade lemonade",
#     "Host a movie night under the stars",
#     "Go to the beach or pool",
#     "Take a road trip",
#     "Have a technology-free day",
#     "Visit a new city or town",
#     "Try a new summer recipe",
#     "Attend a summer festival or fair",
#     "Make s'mores over a fire",
#     "Go stargazing",
#     "Volunteer for a local cause",
#     "Create a summer playlist and dance to it"
#     "Read a book outside"
    
# ]

# # Create a printable checklist PDF
# class PDF(FPDF):
#     def header(self):
#         self.set_font("Arial", "B", 16)
#         self.cell(0, 10, "Summer Bucket List 2025", ln=True, align="C")
#         self.ln(10)

#     def add_checklist(self, items):
#         self.set_font("Arial", "", 12)
#         for item in items:
#             self.cell(10, 10, u"\u2611", border=0)  # Checkbox
#             self.cell(0, 10, item, ln=True)

# pdf = PDF()
# pdf.add_page()
# pdf.add_checklist(bucket_list_items)

# # Save the PDF
# output_path = "/mnt/data/Summer_Bucket_List_2025_Checklist.pdf"
# pdf.output(output_path)
# output_path


# from openai import OpenAI

# client = OpenAI(
#     base_url="https://api.targon.com/v1",
#     api_key=""
# )

# try:
#     response = client.chat.completions.create(
#         model="ModelCloud/DeepSeek-V3-0324-BF16",
#         stream=True,
#         messages=[
#             {"role": "system", "content": "You are a helpful programming assistant."},
#             {"role": "user", "content": "Write a bubble sort implementation in Python with comments explaining how it works"}
#         ],
#         temperature=0.7,
#         max_tokens=256,
#         top_p=0.1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     for chunk in response:
#         if chunk.choices[0].delta.content is not None:
#             print(chunk.choices[0].delta.content, end="")
# except Exception as e:
#     print(f"Error: {e}")


# visual recognition
import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {openrouter_api_key}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "qwen/qwen2.5-vl-72b-instruct:free",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What is in this image?"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            }
          }
        ]
      }
    ],
    
  })
)

print(response)