import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from Src.mcqgenerator.utils import read_file,get_table_data
from Src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from Src.mcqgenerator.logger import logging
import streamlit as st
from langchain.callbacks import get_openai_callback



with open('C:/Users/sou09/genAI_mcq/Response.json', 'r') as file:
    RESPONSE_JSON=json.load(file)

# creating a title for the APP
st.title('MCQs Creator Application')

# Create a form using st.form
with st.form('user_inputs'):

    uploaded_file=st.file_uploader('Upload a PDF or text file')

    # Input Fields

    mcq_count=st.number_input('No of MCQs',min_value=3, max_value=50)

    subject=st.text_input('Insert Subject', max_chars=20)

    difficulty=st.text_input('Complexity Level of Questions',max_chars=20)

    # Add button
    button=st.form_submit_button('Create MCQs')    

    # Check if button is clicked 

    if button and uploaded_file is not None and mcq_count and subject and difficulty:

        with st.spinner('Loading..'):
            try:
                text=read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {

                            "text":text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":difficulty,
                            "response_json":json.dumps(RESPONSE_JSON)
                           }
                    )

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error('Error')

            else:

                if isinstance(response, dict):

                    quiz=response.get('quiz',None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)

                        if table_data is not None:
                            table_data=get_table_data(quiz)

                            if table_data is not None:
                                df=pd.DataFrame(table_data)
                                df.index=df.index+1
                                st.table(df)

                                st.text_area(label="Review",value=response['review'])

                            else:
                                st.error("Error in the table data")

                else:
                    st.write (response)








