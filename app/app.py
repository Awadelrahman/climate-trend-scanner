import streamlit as st
import torch
import os
import uvicorn
import logging
from typing import List
from trends_innovations_classifier.models.transformer import TransformerTandIClassifier
from entity_networks_extractor.entity_extraction import EntityExtractor
import warnings
import pandas as pd
warnings.filterwarnings("ignore")


st.set_page_config(layout="centered") #"wide"
# Centering the logo and the title
col1, col2, col3 = st.columns([1,1,1])
with col2:
    # Display the logo
    st.image("app/logo.png", width=320)  # Adjust the width as per your logo size
st.divider()

    # Display the title
st.markdown("<h1 style='text-align: center;'>Trends Innovation Classifier</h1>", unsafe_allow_html=True)

# User text inputs
user_input = st.text_area("Enter some text and press Ctrl + Enter", height=200)

class Sample:
    def __init__(self, text):
        self.text = text


def load_model():
    if os.path.exists(f"app/trends_innovations_classifier/checkpoints/distilbert-base-uncased"):
        model = TransformerTandIClassifier(model_name="distilbert-base-uncased",
            # TODO: create a default config somewhere else instead of hard coding it here
            model_config={"device": 'cuda' if torch.cuda.is_available() else 'cpu', "num_labels": 17})
    else:
        raise Exception("No model checkpoint found. Please train a model first.")
    
    return model

MODEL=load_model()
#def predict(samples: List[Sample]) -> List[str]:
def predict(user_input):
    """
    Entrypoint for predicting the labels of a list of samples
    :param user_input: the text input from the user
    :return: a list with a label for each sample
    """
    # Creating a Sample object from user input
    sample = Sample(user_input)

    # In this case, we have only one sample
    samples = [sample.text]

    # Call your model's predict function
    predictions = MODEL.predict(samples)
    return predictions #predictions

# Displaying the user input
if user_input:
    prediction=predict(user_input)[0]
    # st.markdown(f'<p style="color:red; font-size: 24px;">Text Class:</p>', unsafe_allow_html=True)
    st.subheader("Text Class:")
    col21, col22, _, = st.columns([1,1,1])
    with col21:
        tab_spaces=" ".join(6*["&nbsp"])
        st.markdown(f'<p style="color:brown; font-size: 28px;">{tab_spaces} {prediction}</p>', unsafe_allow_html=True)


st.divider()
st.markdown("<h1 style='text-align: center;'>Name Entities</h1>", unsafe_allow_html=True)

x = EntityExtractor()

if user_input:

    annotations = x.get_annotations(user_input)
    annotations_df=pd.DataFrame(annotations,columns=['Entity', 'Entity Type', 'Attributes'])

    st.dataframe(annotations_df, width=1000)



st.divider()

st.markdown("<h1 style='text-align: center;'>Entity Network</h1>", unsafe_allow_html=True)

image_path = 'app/entity_networks_visualizer/graph.png'


st.image(image_path)  # Adjust the width as per your logo size