import numpy as np
from keras.models import model_from_json
import cv2
import urllib.request
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
        # load weights into new model
        loaded_model.load_weights(conf.model_path+"top_model_weights.h5")
        return loaded_model

    def prepere_data(self, images_url=[]):
        # Obtain images and resizing
        testImgs = []
        for img in images_url:
            with urllib.request.urlopen(img) as url:   
                arr = np.asarray(bytearray(url.read()), dtype=np.uint8)
                testImgs.append(cv2.resize(cv2.imdecode(arr, -1), (150, 150)))

        testImgs = np.asarray(testImgs)
        testImgs = testImgs / 255
        return testImgs

    def img_classification(self, images_url=[]):
        imgs_data = self.prepere_data(images_url)
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