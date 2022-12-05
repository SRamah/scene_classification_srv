import numpy as np
from keras.models import model_from_json
import cv2
import requests
from urllib import request
import os
import plugins.scenes.params as conf

class SceneClassification:
    def __init__(self):
        self.scenes_index = conf.scenes_index
        self.model = self.load_model()

    def load_model(self):
        # Loaded model from disk
        json_file = open(conf.model_path+'model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        model_file_path = conf.model_path+"top_model_weights.h5"
        # Check whether a path pointing to a file
        if not os.path.isfile(model_file_path):
            request.urlretrieve(conf.model_file_url, model_file_path)
        else:
            # load weights into new model
            loaded_model.load_weights(model_file_path)
        return loaded_model

    def prepere_data(self, images_url=[]):
        # Obtain images and resizing
        testImgs = []
        for img in images_url:
            res = requests.get(img, stream=True)
            if res.status_code == 200:
                arr = np.asarray(bytearray(res.raw.read()), dtype=np.uint8)
                testImgs.append(cv2.resize(cv2.imdecode(arr, -1), (150, 150)))
            else:
                pass
        testImgs = np.asarray(testImgs)
        testImgs = testImgs / 255
        return testImgs

    def img_urls_classification(self, images_url=[]):
        imgs_data = self.prepere_data(images_url)
        scenes_pred = self.model.predict(imgs_data)
        scenes_ids = np.argmax(scenes_pred, axis = 1)
        get_label = lambda index: self.scenes_index.get(index)
        format_scores = lambda s: {get_label(i):round(float(s[i]),2) for i in range(len(s))} 
        results = [{'image_url':images_url[i], 
                    'scene_label':get_label(scenes_ids[i]),
                    'scores':format_scores(scenes_pred[i])} for i in range(len(images_url))]
        return results

    def img_obj_classification(self, img_obj=[]):
        img_arr = np.asarray(bytearray(img_obj), dtype=np.uint8)
        imgs_data = [cv2.resize(cv2.imdecode(img_arr, -1), (150, 150))]
        scenes_pred = self.model.predict(imgs_data)
        scenes_ids = np.argmax(scenes_pred, axis = 1)
        get_label = lambda index: self.scenes_index.get(index)
        format_scores = lambda s: {get_label(i):round(float(s[i]),2) for i in range(len(s))} 
        results = [{'image_url':images_url[i], 
                    'scene_label':get_label(scenes_ids[i]),
                    'scores':format_scores(scenes_pred[i])} for i in range(len(images_url))]
        return results


if __name__ == "__main__":
    images_url = ["https://storage.googleapis.com/yk-cdn/photos/pdp/adam-burton/valley-of-the-ten-peaks.jpg",
             "https://img.freepik.com/photos-gratuite/belle-photo-foret-grands-arbres-verts_181624-20615.jpg"]
    SC = SceneClassification()
    results = SC.img_classification(images_url)
    print(results)