FROM ubuntu

RUN apt-get update
RUN apt-get install python-pip

ADD . /tmp/
RUN python /tmp/setup.py install

RUN rm -rf /tmp/*
