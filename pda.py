import streamlit as st
import time
from groq import Groq
import dotenv
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
    
def get_rephrased_text(input_text):
    instructions = open('./instruction.txt', 'r').read()
    system = f"You are a child psychologist who helps adults speak effectively to children with Pathalogical Demand Avoidance. Here is some knowledge about PDA communication: {instructions}\n\n"
    prompt = f"{system} Think step-by-step, THEN rephrase the following text (after you are done thinking step by step) for speaking with someone who has Pathological Demand Avoidance, using the provided knowledge about PDA communication: ```{input_text}```. The revised text should be the last thing you provide, nothing after it."
    
    response = llm(prompt)
    first_pass_response = response
    extract_prompt = f"Reponse content: ```{first_pass_response}```I need help extracting the rewritten phrase from this response. Can you please tell me ONLY what the rephrased text is?"
    response = llm(extract_prompt)
    return response

def choose_best_response(responses):
    #responses is an array of llm responses
    instructions = open('./instruction.txt', 'r').read()
    system = f"You are a child psychologist who helps adults speak effectively to children with Pathalogical Demand Avoidance. Here is some knowledge about PDA communication: {instructions}\n\n"

    evaluate_prompt = f"Reponse content: ```{responses}```I need help choosing the best rewritten phrase from these responses. Rank the responses (no duplicate rankings). There must be a clear winnder. Provide the explanation first, before choosing a winner."

    # add other llm options here
    # response = ollama.chat(model='llama3:latest', messages=[
    #    {
    #        'role': 'user',
    #        'content': prompt,
    #    },
    #])
    #return response['message']['content']

# Create Streamlit app
st.title("Rephrase Text for PDA-Friendly Communication")
with st.expander("About"):
    st.markdown("From https://www.autismbc.ca/blog/resource-guide/pathological-demand-avoidance-pda-explained/")
    st.markdown("> Pathological Demand Avoidance (PDA) is an autistic profile. PDA individuals share autistic characteristics and also have many of the ‘key features’ of a PDA profile. It is most widely recognized in the UK. PDA is best explained as an extreme avoidance of everyday activities, refusal of demands and challenges with authority due to severe anxiety. In the United States and Canada, PDA is still emerging and not widely diagnosed by professionals due to lack of awareness.")
    st.markdown("This streamlit app helps you rephrase your language for effectively communicating with kids with PDA.")
    st.markdown("Check out the source on github: https://github.com/gavinblair/pathological-demand-avoidance")

# Text input
input_text = st.text_area("Enter text to rephrase:")

if st.button("Rephrase"):
    start_time = time.time()
    with st.spinner("Thinking..."):
        responses  = []  # Initialize an empty list for responses

        # Get three responses
        for _ in range(2):
            response = get_rephrased_text(input_text)
            responses.append(response)  # Append the rephrased text to the list

        response = choose_best_response(responses)
    
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


