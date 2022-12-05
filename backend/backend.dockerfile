FROM gcr.io/kaggle-images/python:v122

RUN useradd -rm -d /home/ramah -s /bin/bash -g root -G sudo -u 1001 ramah
USER ramah
WORKDIR /home/ramah

EXPOSE 8000

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

RUN chmod +x entrypoint.sh