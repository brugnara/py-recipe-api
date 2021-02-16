FROM python:3

MAINTAINER brugnara

ENV PYTHONUNBUFFERED 1


#RUN apk add --update --no-cache \
#  postgresql-client \
#  postgresql-dev \
#  build-base
RUN apt update && apt install -y prostgresql-client

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
