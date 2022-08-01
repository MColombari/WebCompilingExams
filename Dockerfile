FROM ubuntu:latest

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

COPY . /app
RUN pip install -r requirements.txt

CMD python3 run.py