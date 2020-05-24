FROM python:3

RUN pip install --upgrade pip
RUN pip install \
    django==2.1 \
    pika \
    Pillow

EXPOSE 8000

WORKDIR /webserver
COPY . /webserver

ENV FP_MEDIA "/media/"
ENV FP_RABBITMQ_QUEUE images
ENV FP_RABBITMQ_HOST localhost
RUN python3 manage.py migrate
CMD python3 manage.py runserver 0.0.0.0:8000
