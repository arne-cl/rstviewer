FROM nlpbox/nlpbox-base:16.04

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y python-pip phantomjs && \
    pip2 install selenium

WORKDIR /opt
RUN git clone https://github.com/arne-cl/rstviewer.git

WORKDIR /opt/rstviewer
RUN python2 setup.py install

ENTRYPOINT ["rstviewer"]
