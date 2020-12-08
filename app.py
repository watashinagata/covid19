import streamlit as st
import requests
import pandas as pd
import numpy as np

st.title('covid19感染者数')

url = 'https://opendata.corona.go.jp/api/Covid19JapanAll'
#https://corona.go.jp/dashboard/
response = requests.get(url)
json_data = response.json()

pref_namelist = pd.read_csv("./pref_code.csv", header=None).values.T.tolist()



st.header('累計感染者数（県別）')
prefectures = st.multiselect('県を選択',pref_namelist[0],["東京都"])


df_plot = pd.DataFrame()
for pref in prefectures:
    cols = ['date', pref]
    df = pd.DataFrame(index=[], columns=cols)

    for i in range(len(json_data['itemList'])):
        if json_data['itemList'][i]['name_jp'] == pref:
            data = json_data['itemList'][i]['date']
            npatient = int(json_data['itemList'][i]['npatients'])


            record = pd.Series([data, npatient],index=df.columns)
            df = df.append(record, ignore_index=True)
    df.drop(df.tail(1).index,inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    
    if len(df_plot) == 0:
        df_plot = df
    else:
        df_plot = df_plot.merge(df, how='outer', on='date')


df = df.sort_values('date', ascending=True)
df_plot = df_plot.set_index("date")


agree = st.checkbox('表を表示する')
if agree:
    df_plot


st.line_chart(df_plot)
