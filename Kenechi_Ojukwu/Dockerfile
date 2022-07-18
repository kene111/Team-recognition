#FROM python:3.7-slim-buster
FROM ubuntu:18.04 as builder

RUN apt-get -y update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
         python3.6 \
         python3-pip \
         python3-dev \
         python3-setuptools \
         wget \
         build-essential \
         gcc \
         libpq-dev \
         nginx \
         ca-certificates \
         python3-opencv \
         python3-tk \
         git \
         sudo \
         cmake \
         ninja-build \
         && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /ps/challenge


# Detectron2 prerequisites
RUN pip3 install --upgrade pip
RUN pip3 install Pillow==6.2.2 
RUN pip3 --no-cache-dir install torch==1.9.0+cpu torchvision==0.10.0+cpu  -f https://download.pytorch.org/whl/torch_stable.html

# CPU
#RUN pip3 --no-cache-dir install torch torchvision

# CUDA compiled
#RUN pip3 --no-cache-dir install install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu113

### Detectron2 
# CPU
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html 

# CUDA compiled
#RUN pip3 install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html

# Other Libraries
RUN pip3 install numpy scikit-learn scikit-image
RUN pip3 install filterpy tk
RUN pip3 install opencv-python

COPY . /ps/challenge


CMD ["sh"]
