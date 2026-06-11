# import os
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("models/gemini-2.5-flash")


# def ask_question(question,context,history):

#     prompt = f"""
# You are a Forex Research Assistant.

# Answer ONLY from the supplied report context.

# Conversation History:
# {history}

# Document Context:
# {context}

# Current Question:
# {question}

# Instructions:

# 1. Use report context.
# 2. Use conversation history when needed.
# 3. If answer is not available in report,
#    respond:

#    Information not found in report.
# """

#     response = model.generate_content(
#         prompt
#     )

#     return response.text

import google.generativeai as genai

model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_response(prompt):

    response = model.generate_content(
        prompt
    )

    return response.text