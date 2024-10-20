import json
import pika
import logging

logging.getLogger("pika").setLevel(logging.ERROR)

host_name = 'localhost'

class Emit:
    def send(self, id, action, payload):
        self.connect()
        self.publish(id, action, payload)
        self.close()

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name)
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='grades',
                                      exchange_type='topic')

    def publish(self, id, action, payload):
        routing_key = f"grade.{id}.{action}"
        message = json.dumps(payload)

        self.channel.basic_publish(exchange='grades',
                                   routing_key=routing_key,
                                   body=message)

    def close(self):
        self.connection.close()

class Receive:
    def __init__(self):
        logging.info("Waiting for messages...")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host_name)
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='grades',
                                      exchange_type='topic')

        self.channel.queue_declare('grade_event_queue', exclusive=True)
        self.channel.queue_bind(exchange='grades', queue='grade_event_queue', routing_key="grade.*.*")
        self.channel.basic_consume(queue='grade_event_queue', on_message_callback=self.callback)

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        logging.info(f"Calificación del usuario modificada")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    Receive()