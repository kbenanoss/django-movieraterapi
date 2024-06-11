# Use the official Python image as a base
FROM python:3.11.4-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]
