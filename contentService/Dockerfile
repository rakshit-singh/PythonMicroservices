FROM python:3.9
ENV PYTHONENV 1

# RUN apk add --update postgresql-client
# RUN apk add --update --no-cache --virtual .tmp-build-deps \
# 	gcc libc-dev linux-headers postgresql-dev

# RUN apk add --update --no-cache py3-pandas

WORKDIR /contentService
COPY requirements.txt /contentService/requirements.txt
RUN pip install -r requirements.txt
# RUN apt-get update && apt-get install -y netcat
COPY . /contentService
# CMD python manage.py runserver 0.0.0.0:8000
