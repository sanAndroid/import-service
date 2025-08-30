import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='wineries_message', durable=True)

message = {
    "name": "Test Winery",
    "url": "https://www.weingut-keller.de/"
}

channel.basic_publish(exchange='',
                      routing_key='wineries_message',
                      body=json.dumps(message))

print(" [x] Sent 'Hello World!'")
connection.close()