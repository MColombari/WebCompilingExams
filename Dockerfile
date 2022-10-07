FROM ubuntu:latest

EXPOSE 5000

RUN apt update && apt -y install \
    python3 \
    python3-pip \
    default-jre \
    default-jdk

RUN mkdir /app
WORKDIR /app

COPY ./webcompilingexams /app/webcompilingexams

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:5000 --log-level=info webcompilingexams:app
# CMD python3 run.py