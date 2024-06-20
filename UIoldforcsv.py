# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:58:09 2024
Use chatgpt environment in my laptop
Test gpt API and streamlit
@author: Tina.T.Zhao
"""


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st




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
    
# testfile=r'C:\Users\Tina.T.Zhao\projects\powermarket\scripts\chatgptforfund\Capacity Factors_for test.csv'
# testdf=load_csv(testfile)
# plot_data(testdf)




st.title('Fundamental  Data Analyzer')
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# if uploaded_file is not None:
#     data = load_csv(uploaded_file)
#     st.write(data.head())
#     plot_data(data)
    
    
if uploaded_file is not None:
    try:
        data = load_csv(uploaded_file)
        st.write(data.head())
        plot_data(data)
    except ValueError as e:
        st.error(f"Error: {e}")
        


