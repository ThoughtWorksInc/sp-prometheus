FROM ubuntu

RUN apt-get update
RUN apt-get install -y python-pip

ADD . /tmp/
WORKDIR /tmp/
RUN  python setup.py install

RUN rm -rf /tmp/*
