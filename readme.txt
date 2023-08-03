docker build -t dj1 .
<<<<<<< HEAD
docker run -p 8000:8000 --name C-dj1 -it dj1 bash
=======

docker run -p 8000:8000 --name C-dj1 -d dj1 bash

################ mine ##############

FROM ubuntu:20.04

RUN apt update -y 
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install vim -y


COPY ./requirements.txt .
RUN pip3 install -r requirements.txt 


WORKDIR /app

COPY . .



COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]



############ vikas #################

# pull official base image
FROM repo.npci.org.in/python:3.8.10


# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# COPY ./requirements.txt .
COPY . /usr/src/
RUN  pip install --trusted-host repo.npci.org.in -i https://centos79:dtcDr7TQBiMdWFIdrY@repo.npci.org.in/repository/python-remote/simple -r requirements.txt



COPY ./entrypoint.sh /usr/src/
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
>>>>>>> 351522e65a5b1b9d0a91d17e35879760be95e5d1
