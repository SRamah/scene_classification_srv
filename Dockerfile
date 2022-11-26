FROM gcr.io/kaggle-images/python:v122

EXPOSE 8000

WORKDIR /workspace

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

RUN wget https://mys3db.s3.eu-west-3.amazonaws.com/public_repo/Scene_Classification_Models/cnn/top_model_weights.h5

RUN mv top_model_weights.h5 ./plugin/scenes/algos/cnn 

CMD uvicorn --host=0.0.0.0 main:app --reload