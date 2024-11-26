import pika
import json
import time
import logging

logging.getLogger("pika").setLevel(logging.ERROR)

class Emit:

    def send(self, routing_key, payload):
        self.connect()
        self.publish(routing_key, payload)
        self.close()

    def connect(self):
        while True:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
                print("Conectado a RabbitMQ")
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange='grade_exchange',
                                              exchange_type='topic')
                return
            except pika.exceptions.AMQPConnectionError:
                print("Esperando a que RabbitMQ esté disponible...")
                time.sleep(5)

    def publish(self, routing_key, message):
        self.channel.basic_publish(
            exchange='grade_exchange',
            routing_key=routing_key,
            body=json.dumps(message)
        )
    
    def close(self):
        self.connection.close()

class Receive:
    def __init__(self):
        logging.info("Waiting for messages...")
        while True:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
                break
            except:
                print("Esperando a que RabbitMQ esté disponible...")
                time.sleep(5)

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='grade_exchange',
                                      exchange_type='topic')

        self.channel.queue_declare('grade_event_queue', exclusive=True)
        self.channel.queue_bind(exchange='grade_exchange', queue='grade_event_queue', routing_key="grade.*.*")
        self.channel.basic_consume(queue='grade_event_queue', on_message_callback=self.callback)

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        body = json.loads(body)
        logging.info(f"Mensaje '{method.routing_key}'")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    Receive()