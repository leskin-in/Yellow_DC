#!/usr/bin/env python3

import pika
import os
import time

from morphing import face_to_fruits


RABBITMQ_QUEUE = os.environ['FP_RABBITMQ_QUEUE']
RABBITMQ_HOST = os.environ['FP_RABBITMQ_HOST']


connection = None
channel_receive = None

def _prepare():
    """
    Prepare pika connection
    """
    global connection
    global channel_receive

    if connection is not None:
        return

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))

    channel_receive = connection.channel()
    channel_receive.queue_declare(queue=RABBITMQ_QUEUE)


def _callback(channel, method, properties, body):
    path = body.decode('utf-8')
    print('Received request for \'{}\''.format(path))

    if not os.path.isfile(path):
        print('Not a file: \'{}\''.format(path))
        return

    resulting_path = path + '.proc' + os.path.splitext(path)[1]

    t_start = time.perf_counter()
    face_to_fruits(path, resulting_path)
    t_end = time.perf_counter()
    print('Result is saved to \'{}\'. Elapsed: {:10.3f}'.format(resulting_path, t_end - t_start))


def main():
    global channel_receive

    _prepare()
    channel_receive.basic_consume(RABBITMQ_QUEUE, _callback, auto_ack=True)
    channel_receive.start_consuming()


if __name__ == '__main__':
    main()
