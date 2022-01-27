FROM python:3.9
ENV PYTHONENV 1



WORKDIR /userInteractionService
COPY requirements.txt /userInteractionService/requirements.txt
RUN pip install -r requirements.txt
# RUN apt-get update && apt-get install -y netcat
COPY . /userInteractionService
# CMD python manage.py runserver 0.0.0.0:8000

