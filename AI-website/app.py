import streamlit as st
import numpy as np
import pandas as pd
from groq import Groq
import os
import io
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode


st.markdown(
    """
    <style>
    @keyframes rainbow {
      0%   { background-position:   0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position:   0% 50%; }
    }
    .matrix-ai-title {
      font-size: 4rem;
      font-weight: bold;
      /* gradient background */
      background: linear-gradient(-45deg,
        #00ff00,
        #00ffff,
        #ffffff,
        #00ff00);
      background-size: 400% 400%;
      /* make the text show the gradient */
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      /* animate the gradient */
      animation: rainbow 6s ease infinite;
      text-align: center;
      margin: 2rem 0;
    }
    </style>
    <h1 class="matrix-ai-title">MATRIX-AI</h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: #00ff00; }
        }
        
        .welcome-text {
            font-family: monospace;
            font-size: 0.7rem;
            color: #00ff00;
            overflow: hidden;
            white-space: nowrap;
            margin: 0 auto;
            letter-spacing: .15em;
            border-right: .15em solid #00ff00; /* The cursor */
            animation: 
                typing 3.5s steps(40, end),
                blink-caret .75s step-end infinite;
        }
        
        .welcome-container {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
            width: 100%;
        }
    </style>

    <div class="welcome-container">
        <div class="welcome-text">
            Welcome to Matrix-AI, AI that you want for business not just for chatting!!
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

user_query      = st.text_input("HIT THE MATRIX")
uploaded_files  = st.file_uploader(
    "Choose 1 to 5 text files", type="txt", accept_multiple_files=True
)
num_files       = len(uploaded_files)
num_columns     = 5
prompt          = str()
if st.button('Analyze'):
    if len(user_query) == 0:
        st.warning("Query cannot be empty.")
        st.stop()

    # Check if the user uploaded at least one file
    if not uploaded_files:
        st.warning("Please upload at least one text file to proceed.")
        st.stop()  # Stops the app here until files are uploaded

    for uploaded_file in uploaded_files:
        # Wrap the uploaded file in a TextIOWrapper to read as text
        stringio = io.StringIO(uploaded_file.read().decode("utf-8"))
        text_data = stringio.read()

        prompt += "File name: " + uploaded_file.name + "\n"
        prompt += "File content: " + text_data + "\n\n"
    
    prompt += "My Application user input: " + user_query + "\n\n"

    prompt += "My instructions to you:\n"
    prompt += "i) Generate " + str(num_columns) + " columns names for my matrix AI, where first column should be (Item), last column should be (what is missing?), and reamining columns should be top essentials columns to compare the content in files" + "\n"
    prompt += "ii) Your output should not have any other content, only csv, I will directly take your output to parse into pandas data frame" + "\n"
    prompt += "iii) Include analaysis + data in each cell, be crisp and concise, do not club different things in one column, take top columns and take user request into consideration" + "\n"

    groq_api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key = groq_api_key)
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None, 
    )

    # Collect streamed chunks into a single string
    csv_output = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            csv_output += content

    df = pd.read_csv(io.StringIO(csv_output))

    st.write(df)