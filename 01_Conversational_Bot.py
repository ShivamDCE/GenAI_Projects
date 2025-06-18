from groq import Groq
from dotenv import load_dotenv
import os

api_key= os.getenv('GROQ_API_KEY')
#print(api_key)
client = Groq(api_key=api_key)

history = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]
def conversation(msg, conv=history):
    print(conv)
    conv.append({
            "role":"user",
            "content":msg
        })
    #print(current_txt)
    chat_completion = client.chat.completions.create(
        messages=conv,
        model="llama-3.3-70b-versatile"
    )
    llm_response = chat_completion.choices[0].message.content
    print(llm_response)
    conv.append({
        "role":"assistant",
        "content":llm_response
    })
    return llm_response

# Print the completion returned by the LLM.
conversation("Which country has the highest GDP?")
print(history) 