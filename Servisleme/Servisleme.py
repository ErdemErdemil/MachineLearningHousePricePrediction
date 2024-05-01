#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import joblib

excel_filepath = r"C:\Users\erdem\X\X_Emlak_Verileri_Onislenmis.xlsx"
df = pd.read_excel(excel_filepath)

df.dropna(inplace=True)

X = df.drop("fiyat", axis=1)
y = df["fiyat"]
y = y.fillna(y.mean())

model = GradientBoostingRegressor()  
model.fit(X, y)

trained_columns = X.columns.tolist()

model_filename = "x_test_model.pkl"
joblib.dump(model, model_filename)
joblib.dump(trained_columns, 'x_trained_columns.pkl')


# In[11]:


import streamlit as st
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import joblib

model = joblib.load("C:\\Users\\erdem\\X\\Servisleme\\x_test_model.pkl")

trained_columns = joblib.load("C:\\Users\\erdem\\X\\Servisleme\\x_trained_columns.pkl")

st.sidebar.header("Emlak Tahmini Uygulaması")
features = {}
for column in trained_columns:
    features[column] = st.sidebar.number_input(f"Enter {column}", value=0)

input_data = pd.DataFrame([features])
prediction = model.predict(input_data)[0]

st.write(f"**Tahmini Fiyat:** {prediction:.2f} TL")


# In[ ]:




