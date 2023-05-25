FROM nvidia/cuda:11.0-base
RUN apt-get update && apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt install -y python3.8
RUN apt install -y python3-pip
RUN apt install -y git
COPY requirements_v2.txt /usr/local/bin
RUN pip3 install -r /usr/local/bin/requirements_v2.txt
RUN pip3 install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
COPY nnUNet/ /usr/local/bin/nnUNet/
COPY trained_models /usr/local/bin/trained_models/
RUN pip3 install -U setuptools
RUN pip3 install -e /usr/local/bin/nnUNet
ENV RESULTS_FOLDER=/usr/local/bin/trained_models/
COPY inference_v2.py /usr/local/bin

ENTRYPOINT ["python3", "/usr/local/bin/inference_v2.py"]