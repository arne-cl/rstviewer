FROM nlpbox/nlpbox-base:16.04

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y python-pip phantomjs && \
    pip2 install selenium pudb

ADD pudb.cfg /root/

WORKDIR /opt
RUN git clone https://github.com/arne-cl/rstviewer.git

WORKDIR /opt/rstviewer
RUN python2 setup.py install

# workaround for PhantomJS error "QXcbConnection: Could not connect to display "
ENV QT_QPA_PLATFORM offscreen

ENTRYPOINT ["rstviewer"]
