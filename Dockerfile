FROM python:3.7.10-buster
MAINTAINER Rus Jr

ENV PYTHONPATH=/src
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Almaty
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /src
ADD requirements.txt /src/
RUN pip install -r /src/requirements.txt

WORKDIR /src
CMD python worker.py
