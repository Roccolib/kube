from ubuntu:focal
#maintainer of the image
LABEL maintainer="Richard"
#create directory
RUN mkdir /bases
#copiying source code to container
ADD https://github.com/Roccolib/kube/blob/main/orchestre.py ./bases/pythonfiles/
#home directory for container
WORKDIR /bases/pythonfiles
#install python 3.9
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/* &&\
    add-apt-repository ppa:deadsnakes/ppa && apt-get update &&\
    apt-get install -y software-properties-common &&\
    apt-get update &&\
    apt-get install -y python3.9
RUN alias python=python3.9
#add pip to install dependencies
RUN apt-get install -y python3-pip &&\
    pip3 install flask && pip3 install requests && pip3 install kafka-python
#expose port 5000
#expose 5000
