FROM python:3.6

RUN apt-get update

# Install Git
RUN apt-get install -y git

# Install Wrk
RUN echo "===> Installing  tools..."  && \
    apt-get -y install build-essential curl && \
    \
    echo "===> Installing wrk" && \
    WRK_VERSION=$(curl -L https://github.com/wg/wrk/raw/master/CHANGES 2>/dev/null | \
                  egrep '^wrk' | head -n 1 | awk '{print $2}') && \ 
    echo $WRK_VERSION  && \
    mkdir /opt/wrk && \
    cd /opt/wrk && \
    curl -L https://github.com/wg/wrk/archive/$WRK_VERSION.tar.gz | \
       tar zx --strip 1 && \
    make && \
    cp wrk /usr/local/bin/ && \
    \
    echo "===> Cleaning the system" && \
    apt-get -f -y --auto-remove remove build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /opt/wrk/

RUN git clone https://github.com/channelcat/sanic /repository

ADD requirements.txt /req
RUN pip install -r /req && rm /req

ADD . /code

WORKDIR /code
CMD ["python", "main.py"]