FROM python:3.11-slim-bullseye
RUN apt-get update && apt-get upgrade -y && mkdir "/projects" && mkdir "/projects/the_remember_backend"
WORKDIR /projects/the_remember_backend
COPY requiremets/dev.txt .
RUN pip install --upgrade pip && pip install -r dev.txt