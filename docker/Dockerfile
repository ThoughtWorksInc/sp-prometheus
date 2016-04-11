FROM ubuntu

RUN apt-get update
RUN apt-get install -y python-pip

ADD . /tmp/
RUN ls /tmp/
RUN python /tmp/setup.py install

RUN rm -rf /tmp/*
