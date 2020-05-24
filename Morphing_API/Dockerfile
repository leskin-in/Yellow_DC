FROM python:3.7.2

RUN pip install --upgrade pip
RUN pip install \
    matplotlib \
    numpy \
    pika \
    scikit-image \
    torch==1.1.0 \
    torchvision==0.3.0 \
    yacs

WORKDIR /app
COPY . /app

ENV FP_RABBITMQ_QUEUE images
ENV FP_RABBITMQ_HOST rabbit
CMD python3 ml_service.py
