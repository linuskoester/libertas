FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD . /code/ 
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod +x /code/docker/startup.sh
RUN chmod +x /code/docker/wait-for-it.sh

EXPOSE 80