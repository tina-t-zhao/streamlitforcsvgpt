# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:58:09 2024
Use chatgpt environment in my laptop
Test gpt API and streamlit
@author: Tina.T.Zhao
"""

from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import openai
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

import os

#%%

# Set your OpenAI API key
client = OpenAI()  

# simple version of load csv
def load_csv(file_path):
    data = pd.read_csv(file_path)
    return data

def plot_data(data):
    filtered_data = data[data['Year'].between(2020, 2023)]
    plt.figure(figsize=(14, 8))
    colors = plt.cm.tab20.colors
    for i, plant in enumerate(filtered_data['Plant Name'].unique()):
        plant_data = filtered_data[filtered_data['Plant Name'] == plant]
        # Combine Year and Month into a single datetime column for plotting
        plant_data['Year-Month'] = pd.to_datetime(plant_data[['Year', 'Month']].assign(DAY=1))
        plt.plot(plant_data['Year-Month'], plant_data['Wtd Avg Capacity Factor % - Modeled'], marker='o', label=plant, color=colors[i % len(colors)])
    plt.xlabel('Year-Month')
    plt.ylabel('Wtd Avg Capacity Factor % - Modeled')
    plt.title('Wtd Avg Capacity Factor % - Modeled for Different Plants (2020-2023)')
    plt.xticks(rotation=90)
    plt.legend(title='Plant Name')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
    


# Function to summarize the CSV content
def summarize_csv(data):
    summary = f"The dataset contains {data.shape[0]} rows and {data.shape[1]} columns.\n"
    summary += "The columns are:\n"
    for column in data.columns:
        summary += f"- {column}\n"
    return summary



def ask_chatgpt_about_csv(prompt):
   
 
       
    
    response=agent_executor.invoke({"input": prompt})
    
    # example prompt
    # response=agent_executor.invoke({"input": "what's the average Wtd Avg Capacity Factor For different plant in different year?"})
    # response=agent_executor.invoke({"input": "What's the average Wtd Avg Capacity Factor for different Unit ISO Zone in different plant and different year?"})

    # print(response['input'])
    # print(response['output'])
    return response['output']


# test the functions

# testfile=r'C:\Users\Tina.T.Zhao\projects\powermarket\scripts\chatgptforfund\Capacity Factors_for test.csv'
# testdf=load_csv(testfile)
# plot_data(testdf)


st.title('Fundamental Data Analyzer')


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        data = load_csv(uploaded_file)
        st.write(data.head())
        plot_data(data)
        
        # Summarize CSV
        csv_summary = summarize_csv(data)
        st.write("CSV Summary:")
        st.write(csv_summary)
        
        # Check if the table already exists and drop it to avoid conflicts
        if os.path.exists("Newtest1.db"):
            os.remove("Newtest1.db")
           
       #create a SQL agent to interact with it:
        engine = create_engine("sqlite:///Newtest1.db")
        data.to_sql("Newtest1", engine, index=False)
        dbtouse = SQLDatabase(engine=engine)
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        agent_executor = create_sql_agent(llm, db=dbtouse, agent_type="openai-tools", verbose=False)
        
        
    except ValueError as e:
        st.error(f"Error: {e}")



# ChatGPT interaction section
st.header("Ask ChatGPT")
user_input = st.text_input("Ask a question to ChatGPT:")
if st.button("Submit"):
    if user_input:
        with st.spinner("Waiting for response..."):
            response = ask_chatgpt_about_csv(user_input)
            st.write("ChatGPT says:", response)
    else:
        st.warning("Please enter a question!")



#%%
# # Function to load CSV with encoding handling
# def load_csv(file):
#     encodings = ['utf-8', 'latin1', 'utf-16', 'utf-16le', 'utf-16be']
#     for encoding in encodings:
#         try:
#             data = pd.read_csv(file, encoding=encoding, delimiter='\t')
#             st.success(f"Successfully read the file with {encoding} encoding")
#             return data
#         except UnicodeDecodeError:
#             st.warning(f"Failed to read with encoding {encoding}: UnicodeDecodeError")
#         except Exception as e:
#             st.warning(f"Failed to read with encoding {encoding}: {e}")
#     raise ValueError("Unable to read the CSV file with the provided encodings.")

# Function to plot data
# def plot_data(data):
#     filtered_data = data[data['Year'].between(2020, 2023)]
#     plt.figure(figsize=(14, 8))
#     colors = plt.cm.tab20.colors
#     for i, plant in enumerate(filtered_data['Plant Name'].unique()):
#         plant_data = filtered_data[filtered_data['Plant Name'] == plant]
#         # Combine Year and Month into a single datetime column for plotting
#         plant_data['Year-Month'] = pd.to_datetime(plant_data[['Year', 'Month']].assign(DAY=1))
#         plt.plot(plant_data['Year-Month'], plant_data['Wtd Avg Capacity Factor % - Modeled'], marker='o', label=plant, color=colors[i % len(colors)])
#     plt.xlabel('Year-Month')
#     plt.ylabel('Wtd Avg Capacity Factor % - Modeled')
#     plt.title('Wtd Avg Capacity Factor % - Modeled for Different Plants (2020-2023)')
#     plt.xticks(rotation=90)
#     plt.legend(title='Plant Name')
#     plt.grid(True)
#     plt.tight_layout()
#     st.pyplot(plt)
# testfile=r'C:\Users\Tina.T.Zhao\projects\powermarket\scripts\chatgptforfund\Capacity Factors_for test.csv'
# testdf=load_csv(testfile)
# plot_data(testdf)



# Function to ask ChatGPT
# def ask_chatgpt(prompt):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  # Specify the model here, gpt-4 or gpt-4-turbo
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message['content'].strip()


# Function to ask ChatGPT about the CSV content
# def ask_chatgpt_about_csv(prompt, csv_summary):
#     full_prompt = f"Here is a summary of the CSV file:\n{csv_summary}\n\nUser question: {prompt}"
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": full_prompt}
#         ]
#     )
#     return response.choices[0].message['content'].strip()

# # ChatGPT interaction section
# st.header("Ask ChatGPT")
# user_input = st.text_input("Ask a question about the CSV file:")
# if st.button("Submit"):
#     if user_input:
#         with st.spinner("Waiting for response..."):
#             response = agent_executor.invoke({"input": user_input})
#             st.write("ChatGPT says:", response['output'])
#     else:
#         st.warning("Please enter a question!")

# if uploaded_file is not None:
#     data = load_csv(uploaded_file)
#     st.write(data.head())
#     plot_data(data)
    
    
# if uploaded_file is not None:
#     try:
#         data = load_csv(uploaded_file)
#         st.write(data.head())
#         plot_data(data)
#     except ValueError as e:
#         st.error(f"Error: {e}")

# response = client.upload_file(data)




# # ChatGPT interaction section
# st.header("Ask ChatGPT")
# user_input = st.text_input("Ask a question to ChatGPT:")
# if st.button("Submit"):
#     if user_input:
#         with st.spinner("Waiting for response..."):
#             response = ask_chatgpt_about_csv(user_input,csv_summary)
#             st.write("ChatGPT says:", response)
#     else:
#         st.warning("Please enter a question!")

