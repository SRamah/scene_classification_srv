FROM gcr.io/kaggle-images/python:v122

EXPOSE 8000

WORKDIR /workspace

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD uvicorn --host=0.0.0.0 main:app --reload