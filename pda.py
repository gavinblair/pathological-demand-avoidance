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
    if not isinstance(prompt, str) or len(prompt) < 4:
        return "Error: Prompt must be a string with at least 4 characters"

    if model == "groq":
        client = Groq(
            api_key=os.environ.get("GROQ_SECRET_ACCESS_KEY"),
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        if chat_completion.choices and len(chat_completion.choices) > 0:
            return chat_completion.choices[0].message.content
        else:
            return "Error: Unable to generate response"
    # add other llm options here. here's how you use a local ollama model:
    # response = ollama.chat(model='llama3:latest', messages=[
    #    {
    #        'role': 'user',
    #        'content': prompt,
    #    },
    #])
    #return response['message']['content']
    
def get_rephrased_text(input_text):
    instructions = open('./instruction.txt', 'r').read()
    system = f"You are a child psychologist who helps adults speak effectively to children with Pathalogical Demand Avoidance. Here is some knowledge about PDA communication: {instructions}\n\n"
    prompt = f"{system} Think step-by-step, THEN rephrase the following text (after you are done thinking step by step) for speaking with someone who has Pathological Demand Avoidance, using the provided knowledge about PDA communication: ```{input_text}```. The revised text should be the last thing you provide, nothing after it."
    
    response = llm(prompt)
    first_pass_response = response
    extract_prompt = f"Reponse content: ```{first_pass_response}```I need help extracting the rewritten phrase from this response. Can you please tell me ONLY what the rephrased text is?"
    response = llm(extract_prompt)
    return response, first_pass_response

def choose_best_response(responses):
    # print(f"choosing best response from: ```{responses}```")
    #responses is an array of llm responses
    instructions = open('./instruction.txt', 'r').read()
    system = f"You are a child psychologist who helps adults speak effectively to children with Pathalogical Demand Avoidance. Here is some knowledge about PDA communication: {instructions}\n\n"

    evaluate_prompt = f"{system}\nReponse content: ```{responses}```I need help choosing the best rewritten phrase from these responses. The best one follows the rules in the PDA communication information, above. Rank the responses (no duplicate rankings). There must be a clear winnder. Provide the explanation first, before choosing a winner."
    best_response_thoughts = llm(evaluate_prompt)
    print(best_response_thoughts)
    filtered_response = llm(f"You have been helping me extract the selected phrase from this output: ```{best_response_thoughts}```\nWithout explanation or any other text, output the selected phrase here:")
    return filtered_response

def extract_quote_from_response(response):
    matches = re.finditer(r'"(.*?)"', response)
    last_match = None

    for match in matches:
        last_match = match.group(1)
        # You might need to adjust this condition depending on your requirements
        if not last_match:  # or some other condition that makes sense for you
            break

    if last_match is not None:
        return last_match
    
    print(f"No quotes found in ```{response}```")

    return False

def choose_best_thinking_response(final_answer, all_thinking_responses):
    for i, thinking_response in enumerate(all_thinking_responses):
        if final_answer in thinking_response:
            return thinking_response
    return False

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
        all_responses  = []  # Initialize an empty list for responses
        all_thinking_responses = []

        # Get three responses
        for _ in range(2):
            response, thinking_response = get_rephrased_text(input_text)
            all_responses.append(response)  # Append the rephrased text to the list
            all_thinking_responses.append(thinking_response)

        response = choose_best_response(all_responses)
    
    st.write("Rephrased text:")
    
    if not response:
        print(f"No response: ```{response}```")
        st.write("Something went wrong.")
    else:
        final_answer = extract_quote_from_response(response)
        st.markdown(f"> {final_answer}")

        if final_answer:
            thinking_response = choose_best_thinking_response(final_answer, all_thinking_responses)

            # Create an expander at the bottom to display the entire response
            with st.expander("Read more"):
                st.write(thinking_response)


