import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle

# Load the trained model
model = tf.keras.models.load_model('regression_model.h5')

## load the encoder and scaler
with open('onehot_encoder_geo_r.pkl', 'rb') as file:
    label_encoder_geo = pickle.load(file)

with open('label_encoder_gender_r.pkl', 'rb') as file:
    label_encoder_gender = pickle.load(file)

with open('scaler_r.pkl', 'rb') as file:
    scaler = pickle.load(file)


## stremalit app
st.title("Estimated Salary Prediction")

# User input
geography = st.selectbox('Geography', label_encoder_geo.categories_[0])
gender = st.selectbox("Gender", label_encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
exited = st.selectbox('Exited', [0, 1])
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

input_data = pd.DataFrame({
    'CreditScore' : [credit_score],
    'Gender' : [label_encoder_gender.transform([gender])[0]] ,
    'Age' : [age],
    'Exited': [exited],
    'Tenure' : [tenure],
    'Balance' : [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard' : [has_cr_card],
    'IsActiveMember' : [is_active_member]
})

# One - hot encode 'Geography'
geo_encoded = label_encoder_geo.transform([[geography ]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=label_encoder_geo.get_feature_names_out(['Geography']))

# Combine one - hot encode columns with input data
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

# Scale the input data
input_data_scaled = scaler.transform(input_data)

## Predict salary
predictions = model.predict(input_data_scaled)
predictions_salary = predictions[0][0]

st.write(f'Predict Estimated salary : ${predictions_salary: .2f}')