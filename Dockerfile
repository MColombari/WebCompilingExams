FROM ubuntu:latest

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt update
RUN apt -y install default-jre
RUN apt -y install default-jdk

COPY . /app
RUN pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:5000 webcompilingexams:app