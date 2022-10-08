FROM ubuntu:latest

EXPOSE 5000

RUN apt update && apt -y install \
    python3 \
    python3-pip \
    default-jre \
    default-jdk

COPY ./ /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:5000 --log-level=info webcompilingexams:app