FROM ubuntu

RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install docker-py

ADD . /tmp/
WORKDIR /tmp/
RUN  python setup.py install

RUN rm -rf /tmp/*
