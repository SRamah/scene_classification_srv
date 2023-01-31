import requests
import os


def update_access_token():
    url = os.environ['BACKEND_HOST_ADDRESS']+"/api/v1/auth/token/login"

    payload = {
        "email": os.environ['SUPERUSER'],
        "password": os.environ['SUPERUSER_PASSWORD'],
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    token = response.json().get('access_token')
    os.environ['ACCESS_TOKEN'] = "Bearer {token}".format(token=token)
    print(" [X] ACCESS_TOKEN is updated")


def get_label(image_url:str):
    address = os.environ['BACKEND_HOST_ADDRESS']+"/api/v1/scenes/url/label/"
    payload = [image_url]
    headers = {
        "accept": "application/json",
        "Authorization": os.environ['ACCESS_TOKEN'],
        "Content-Type": "application/json"
    }
    try:
        response = requests.request("PUT", address, json=payload, headers=headers).json()
        if isinstance(response, dict) and response.get("detail"):
            ## Update the ACCESS_TOKEN
            update_access_token()
            return get_label(image_url)
        result = response[0]
    except Exception as e:
        print(" [X] Exception at get classified label: ", e)
        result = {}
    return result