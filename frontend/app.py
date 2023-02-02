import streamlit as st
import requests


# Get the file that was uploaded using st.file_uploader
file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

if file:
    # Prepare the POST request
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWRtaW5AZGF0YS5pbyIsImV4cGlyZXMiOjE2NzUyODg1ODkuOTQ5ODE0OH0.HYTRH9ta5Gtu50Ipb1m4E_IPwCIbZUSHpsG2dFfESug',
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    files = {
        'img': file.getbuffer()#open('csm_bas-montreuil-aerien_2f92705e71.jpeg;type=image/jpeg', 'rb'),
    }

    response = requests.post(
        'http://scene-recognition.backend.recipi.io:8081/api/v1/scenes/obj/label/',
        headers=headers,
        files=files,
    )
    # Check the response
    if response.status_code == 200:
        st.write("Image uploaded successfully!")
        result = response.json()
        st.write("Result:", result)
    else:
        st.write("Failed to upload image")

    st.write(response.json())
