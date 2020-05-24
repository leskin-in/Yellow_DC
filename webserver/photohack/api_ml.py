import pika

from .settings import RABBITMQ_QUEUE, RABBITMQ_HOST


def send_to_ml(data: str):
    """
    Send request to ML for processing
    """
    with pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST)) as connection:
        channel_send = connection.channel()
        channel_send.queue_declare(queue=RABBITMQ_QUEUE)

        channel_send.basic_publish(
                exchange='',
                routing_key=RABBITMQ_QUEUE,
                body=data
        )
