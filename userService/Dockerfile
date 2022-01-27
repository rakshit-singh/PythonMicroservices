FROM python:3.9
ENV PYTHONENV 1


WORKDIR /userService
COPY requirements.txt /userService/requirements.txt
RUN pip install -r requirements.txt
# RUN apt-get update && apt-get install -y netcat
COPY . /userService
# CMD python manage.py runserver 0.0.0.0:8000

