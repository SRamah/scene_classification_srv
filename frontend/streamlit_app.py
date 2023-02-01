import streamlit as st
import pandas as pd
import numpy as np
import os, time
from PIL import Image
import streamlit.components.v1 as com

import helpers as classifier


st.title('Image Scene Classification 🤖')
st.write("## How does it work?")
st.write("Add an image of a natural scene and a machine learning model will analyze it and decide what the scene label is - as in the example below:")
st.image(Image.open("images/example-scene-classification.png"), 
        caption="Example of model being run on a buildings scene.", 
        use_column_width=True)
st.write("## Upload your own image")
st.write("**Note:** The model was trained on natural scenes from around the world, divided into 6 categories  `buildings`  `forest`  `glacier`  `mountain`  `sea`  `street`  and therefore will only with those kind of images.")

uploaded_image = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

image_url = ""
with st.container():
    col1, col2 = st.columns([5,3])
    if uploaded_image is None:
        image_url = st.text_input('Or add a URL link', placeholder="https://images/photo.png")
        if image_url:
            col1.image(image_url)
    else:
        # To read image file as a PIL Image:
        image = Image.open(uploaded_image)
        col1.image(image, caption="Uploaded Image.", use_column_width=True)
        
    
    if st.button("Label Prediction") and (image_url or uploaded_image):
        with st.spinner("Doing the math..."):
            ##### Get Classification label ######
            if image_url:
                api_response =  classifier.get_label(image_url)
            else:
                api_response =  classifier.get_label_obj(uploaded_image.getbuffer())
            #####################################
            st.write("It looks like a **"+ str(api_response.get("scene_label")) + "** scene")
            scores = api_response.get("scores")
            scene_bars = """"""
            if scores:
                for label, value in scores.items():
                    scene_bars += """
                        <p>{label}</p>
                        <div class="progress">
                            <div class="progress-bar" style="width:{value}%;">
                            {value}%
                            </div>
                        </div>
                    """.format(label=label, value=int(value*100))
            container_ = """
                    <head>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                        <style>p{style}</style>
                    </head>
                    <div class="container">{scene_bars}</div>""".format(style="{margin-bottom: 0rem; margin-top: 0.3rem;}", scene_bars=scene_bars)
            with col2.container():
                com.html(container_, height=330)

        # Delete file
        if os.path.exists(image_url):
            os.remove(image_url)
        
        st.write(api_response)

st.write("## How is this made?")
st.write("""The ML part is performed by a CNN-based image classification model, previously trained on 14k images of size 150x150 divided into 6 categories
\ this front end (what you're reading) is built with [Streamlit](https://www.streamlit.io/) .""")
