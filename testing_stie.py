# from openai import OpenAI

# client = OpenAI(
#     api_key="AIzaSyCCOu0rGJYoC7h4hPF-quQMn4PftS6HRTU",
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

def code_executor(code_string: str):
    try:
        exec(code_string)
    except Exception as e:
        print(f"Error executing code: {e}")

code_executor("print('Hello, World!')")