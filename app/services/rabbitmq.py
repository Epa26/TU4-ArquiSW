import pika
import json
import time

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
