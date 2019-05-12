FROM python:3.7-alpine
MAINTAINER Fidel Kang

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev zlib zlib-dev \
    graphviz ttf-freefont
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev


RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

# Setup directory structure
RUN mkdir /usr/src/app

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN adduser -D user
USER user

