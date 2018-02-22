FROM nlpbox/nlpbox-base:16.04

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y python-pip phantomjs firefox && \
    pip2 install selenium pudb

# settings for interactive debugging
ADD pudb.cfg /root/

# install geckodriver for headless browsing with selenium
WORKDIR /usr/local/bin
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.19.1-linux64.tar.gz && \
    rm geckodriver-v0.19.1-linux64.tar.gz


WORKDIR /opt
RUN git clone https://github.com/arne-cl/rstviewer.git

WORKDIR /opt/rstviewer
RUN python2 setup.py install

# workaround for PhantomJS error "QXcbConnection: Could not connect to display "
# ENV QT_QPA_PLATFORM offscreen

ENTRYPOINT ["rstviewer"]
