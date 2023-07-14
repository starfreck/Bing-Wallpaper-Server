# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app:app"]

EXPOSE 8000