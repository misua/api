FROM python:3.11-slim

WORKDIR /app

# Install GPG
RUN apt-get update && apt-get install -y gnupg

COPY . /app

RUN apt-get update && apt-get install -y wget && \
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - && \
    echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" > /etc/apt/sources.list.d/elastic-8.x.list && \
    apt-get update && apt-get install -y filebeat && \
    pip3 install pipenv && \
    pipenv --python 3.11 && \
    pipenv install --deploy --ignore-pipfile && \
    pipenv install -r requirements.txt

COPY filebeat.yml /etc/filebeat/filebeat.yml

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["sh", "-c", "service filebeat start && pipenv run flask run --host=0.0.0.0"]


#docker build -t my-python-app .
#docker run -p 5000:5000 my-python-app


#To build the image, run the following command:

#docker build -t kibana-elasticsearch .

#To run the container, run the following command:

#docker run -d --name kibana-elasticsearch -p 5601:5601 kibana-elasticsearch
