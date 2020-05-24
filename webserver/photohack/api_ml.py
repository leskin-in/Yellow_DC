import pika
import logging
import time

from .settings import RABBITMQ_QUEUE, RABBITMQ_HOST


def send_to_ml(data: str):
    """
    Send request to ML for processing
    """
    for _ in range(20):
        try:
            with pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST)) as connection:
                channel_send = connection.channel()
                channel_send.queue_declare(queue=RABBITMQ_QUEUE)
                channel_send.confirm_delivery()

                channel_send.basic_publish(
                        exchange='',
                        routing_key=RABBITMQ_QUEUE,
                        body=data,
                        properties=pika.BasicProperties(content_type='text/plain', delivery_mode=1),
                        mandatory=True
                )
                break
        except pika.exceptions.AMQPConnectionError as e:
            logging.getLogger().exception(e)
            logging.getLogger().info('Retrying in 3 seconds')
            time.sleep(3)
