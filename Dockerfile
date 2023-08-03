
# FROM brahma_ubuntu:latest

FROM ubuntu:20.04
RUN apt update -y 
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install vim -y
RUN apt-get install cron


COPY ./requirements.txt .
RUN pip3 install -r requirements.txt 


WORKDIR /app

COPY . .



COPY ./entrypoint.sh /

ENTRYPOINT [ "sh", "/entrypoint.sh" ]
