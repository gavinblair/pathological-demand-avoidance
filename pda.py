import streamlit as st
import time
from groq import Groq
import dotenv
import ollama
import re
import os

dotenv.load_dotenv()

st.markdown(
    """
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

def llm(prompt, model="groq"):
    print(model)
    if model == "groq":
        client = Groq(
            # This is the default and can be omitted
            api_key=os.environ.get("GROQ_SECRET_ACCESS_KEY"),
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content

    response = ollama.chat(model='llama3:latest', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']

# Create Streamlit app
st.title("Rephrase Text for PDA-Friendly Communication")

# Text input
input_text = st.text_area("Enter text to rephrase:")

if st.button("Rephrase"):
    start_time = time.time()
    with st.spinner("Thinking..."):
        instructions = open('./instruction.txt', 'r').read()
        system = f"You are a child psychologist who helps adults speak effectively to children with Pathalogical Demand Avoidance. Here is some knowledge about PDA communication: {instructions}\n\n"
        prompt = f"{system} Think step-by-step, THEN rephrase the following text (after you are done thinking step by step) for speaking with someone who has Pathological Demand Avoidance, using the provided knowledge about PDA communication: ```{input_text}```. The revised text should be the last thing you provide, nothing after it."
        print("--- Prompt: ---")
        print(prompt)
        print("---")
        
        response = llm(prompt)
        print("--- Response: ---")
        print(response)
        print("---")
        first_pass_response = response
        extract_prompt = f"Reponse content: ```{first_pass_response}```I need help extracting the rewritten phrase from this response. Can you please tell me ONLY what the rephrased text is?"
        print("--- Extract Prompt: ---")
        print(extract_prompt)
        print("---")
        response = llm(extract_prompt)
        print("--- Extract Response: ---")
        print(response)
        print("---")
    
    st.write("Rephrased text:")
    
    matches = re.finditer(r'"(.*?)"', response)
    last_match = None

    for match in matches:
        last_match = match.group(1)
        # You might need to adjust this condition depending on your requirements
        if not last_match:  # or some other condition that makes sense for you
            break

    if last_match is not None:
        st.markdown(f"> {last_match}")

    # Create an expander at the bottom to display the entire response
    with st.expander("Read more"):
        st.write(first_pass_response)


